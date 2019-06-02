import EPUB_Reader.main as epub_lib


class ReaderController:

    def __init__(self, render_routine, db, config, request):
        self.render_routine = render_routine
        self.db = db
        self.config = config
        self.request = request

    # Load reader (not book)
    def reader(self, reader_format):
        # But js needs book_id to determine book to load
        book_id = self.request.args.get("book_id")
        if reader_format.lower() == "epub":
            epub_reader = epub_lib.EPUB_Reader(render_routine=self.render_routine, db=self.db, config=self.config)
            return epub_reader.epub_reader(book_id)

    def book(self, book_id):
        book_format = self.request.args.get("bookFormat")
        section_from = self.request.args.get("sectionFrom")
        section_to = self.request.args.get("sectionTo")
        file_name = self.request.args.get("fileName")
        is_next = self.request.args.get("isNext")
        is_previous = self.request.args.get("isPrevious")
        if book_format.lower() == "epub":
            epub_reader = epub_lib.EPUB_Reader(render_routine=self.render_routine, db=self.db, config=self.config)
            return epub_reader.epub_book(book_id, section_from=section_from, section_to=section_to, file_name=file_name,
                                         is_next=is_next, is_previous=is_previous)
