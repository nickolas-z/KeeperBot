from enum import Enum


class BotCmd(Enum):
    """
    Enum for available commands.
    """

    # TODO: Using dashes in is not a good practice (for tab-completion). Consider using something else instead.
    CLOSE = "close"
    EXIT = "exit"
    HELLO = "@hello"
    CONTACT_ADD = "add-new-contact"
    CONTACT_SHOW_ALL = "all"
    CONTACT_SHOW_PHONES = "@phone"
    ADD_EMAIL = "@add-email"
    ADD_ADDRESS = "@add-address"
    ADD_NOTE = "@add-note"
    EDIT_NOTE = "@edit-note"
    DELETE_NOTE = "@delete-note"
    ADD_TAG = "@add-tags"
    DELETE_TAG = "@delete-tag"
    GET_NOTES_BY_TAG = "@get-notes-by-tag"
    GET_NOTE_BY_TITLE = "@get-note-by-title"
    GET_ALL_NOTES = "@get-notes"
    BIRTHDAY_ADD = "@add-birthday"
    BIRTHDAY_SHOW = "@show-birthday"
    BIRTHDAY_SHOW_ALL = "@show-birthdays"
    HELP = "help"
    SEARCH_BY = "@search-by"
    YES = "@yes"
    NO = "@no"
    EDIT = "edit-contact-info"
    EDIT_CONTACT_PHONE = "@edit-contact-phone"
    DELETE = "@delete-contact-info"
    DELETE_CONTACT = "@delete-contact"
    DELETE_CONTACT_PHONE = "@delete-contact-phone"
    ADD_CONTACT_INFO = "add-contact-info"
    GET_INFO = "get-info"
    SEARCH_INFO = "search-info"
    DELETE_INFO = "delete-menu"
    SHOW_INFO = "show-info"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    @staticmethod
    def get_all_commands(exclude_prefix=None):
        """
        This function returns a list of all available commands or filters them based on the absence of a keyword.
        Args:
            exclude_prefix (str, optional): The prefix to exclude commands by.
                                            If None, all commands are returned.
        Return:
            list: filtered or all available commands.
        """
        if exclude_prefix:
            return [str(cmd) for cmd in BotCmd if exclude_prefix not in cmd.value]
        return [str(cmd) for cmd in BotCmd]
