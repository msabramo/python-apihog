import unittest

import resource
from chegg_api.term import Term
from chegg_api.school import School
from chegg_api.subject import Subject


class TestTerm(unittest.TestCase):

    def test_init_no_args(self):
        term = Term()
        self.assertIsNotNone(term)
        self.assertIsInstance(term, Term)

    def test_init_school_id(self):
        term = Term(school_id=1566473)
        self.assertIsNotNone(term)
        self.assertIsInstance(term, Term)
        self.assertEquals(term.school_id, 1566473)

    def test_filter(self):
        term_list = Term.objects.filter(school_id=1566473)
        self.assertIsNotNone(term_list)
        self.assertIsInstance(term_list, list)
        term = term_list[0]
        self.assertIsInstance(term, Term)
        self.assertEquals(term.school_id, 1566473)


class TestSchool(unittest.TestCase):

    def test_init_no_args(self):
        school = School()
        self.assertIsNotNone(school)
        self.assertIsInstance(school, School)

    def test_init_school_id(self):
        school = School(school_id=1566473)
        self.assertIsNotNone(school)
        self.assertIsInstance(school, School)
        self.assertEquals(school.school_id, 1566473)

    def test_get_school_id(self):
        school = School.objects.get(school_id=1566473)
        self.assertIsNotNone(school)
        self.assertIsInstance(school, School)
        self.assertEquals(school.school_id, 1566473)
        self.assertEquals(school.long_name, u'University of Florida')

    def test_get_pk(self):
        school = School.objects.get(pk=1566473)
        self.assertIsNotNone(school)
        self.assertIsInstance(school, School)
        self.assertEquals(school.school_id, 1566473)

    def test_get_current_terms(self):
        for school_id in [1566473, 1564798]:
            school = School.objects.get(school_id=school_id)
            current_terms = school.current_terms.all()
    
            for current_term in current_terms:
                self.assertEqual(current_term.school_id, school.school_id)

    def test_get_subjects_2(self):
        school = School.objects.get(school_id=1564798)

        subjects = school.get_subjects()

        self.assertIsInstance(subjects, list)

        for subject in subjects:
            self.assertIsInstance(subject, Subject)
            self.assertTrue(hasattr(subject, 'subject_name'))
            self.assertTrue(hasattr(subject, 'subject_code'))


class TestSubject(unittest.TestCase):

    def test_stuff(self):
        subjects = Subject.objects.filter(school_id=1564798)

        self.assertIsInstance(subjects, list)

        for subject in subjects:
            self.assertIsInstance(subject, Subject)
            self.assertTrue(hasattr(subject, 'subject_name'))
            self.assertTrue(hasattr(subject, 'subject_code'))


if __name__ == '__main__':
    unittest.main()
