import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import app


def test_get_paper_display_details_includes_title_authors_and_abstract():
    paper = {
        'title': 'Composite Materials Review',
        'authors': 'Jane Doe, John Smith',
        'abstract': 'This paper studies advanced composites.',
        'source_file': 'paper.pdf',
    }

    details = app.get_paper_display_details(paper)

    assert details['title'] == 'Composite Materials Review'
    assert details['authors'] == 'Jane Doe, John Smith'
    assert details['abstract'] == 'This paper studies advanced composites.'
    assert details['source_file'] == 'paper.pdf'
