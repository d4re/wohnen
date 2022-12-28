# dead simple file-as-nosql thingie.

import json
import logging

logger = logging.getLogger(__name__)


class JsonFile(object):
    def __init__(self, _json, _existing_ids, _cmp_key, _filename):
        self._json = _json  # list
        self._existing_ids = _existing_ids  # set
        self._cmp_key = _cmp_key  # string
        self._filename = _filename
        self._new = []

    @classmethod
    def open(cls, jsonfile, cmp_key="link"):
        try:
            with open(jsonfile, "r") as f:
                j = json.loads(f.read())
                e = set([a[cmp_key] for a in j])
                logger.debug("Loaded {}, {} records".format(jsonfile, len(j)))
                return cls(j, e, cmp_key, jsonfile)
        except IOError:
            logging.info("New jsonfile: {}".format(jsonfile))
            return cls([], set(), cmp_key, jsonfile)

    def has_item(self, item):
        return item[self._cmp_key] in self._existing_ids

    def add_item(self, item):
        """Adds an item to the list. Does not save it to disk.

        Does not update. If the key is found, nothing is changed.

        Told you this was dead simple. self._cmp_key is badly named, but is the
        keys that are compare to determine if its in the list or not.
        """
        if not self.has_item(item):
            self._json.append(item)
            self._existing_ids.add(item[self._cmp_key])
            self._new.append(item)
            return True
        else:
            return False

    def add_list(self, newlist):
        for item in newlist:
            self.add_item(item)

    @property
    def new_item_count(self):
        return len(self._new)

    @property
    def new_items(self):
        return self._new

    def save(self):
        """Simply overwrites the file with self._json"""
        if self.new_item_count > 0:
            try:
                with open(self._filename, "w") as f:
                    f.write(json.dumps(self._json, indent=4, separators=(",", ": ")))
                    # empty the _new list
                    logger.info(
                        "Wrote {} new items to {}".format(
                            self.new_item_count, self._filename
                        )
                    )
                    self._new[:] = []
            except IOError as e:
                logger.error(e)
        else:
            logger.debug("No new items")
