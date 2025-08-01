from nose.tools import assert_equals, assert_not_equal

from .chunk import init, chunkify

init()

def test_chunkify():
    text = "Independence Day (also promoted as ID4) is a 1996 American science fiction action film[2][3] directed by Roland Emmerich and written by Emmerich and Dean Devlin. It stars an ensemble cast that consists of Will Smith, Bill Pullman, Jeff Goldblum, Mary McDonnell, Judd Hirsch, Margaret Colin, Randy Quaid, Robert Loggia, James Rebhorn, and Harvey Fierstein. The film focuses on disparate groups of people who converge in the Nevada desert in the aftermath of a worldwide attack by a powerful extraterrestrial race. With the other people of the world, they launch a counterattack on July 4—Independence Day in the United States."
    chunks = chunkify(text)
    assert_equals(len(list(chunks)), 3)

def test_chunkify_lessthan_60char():
    text = "Independence Day (also promoted as ID4)."
    chunks = chunkify(text)
    assert_not_equal(len(list(chunks)), 0)

def test_chunkify_grouping():
    text = "The cow jumped over the moon. the moon has no air and no animals roaming. shark is a fish. go fish! Water water every where but not a drop to drink. The water molicules has two hydrogen and one oxygen atom. Atoms have electrons orbitting a nucleus"
    chunks = chunkify(text)
    assert_equals(len(list(chunks)), 6)
