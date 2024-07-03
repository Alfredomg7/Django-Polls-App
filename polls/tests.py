import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the given
    number of `days` offset to now (negative for questions published in the past,
    positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):
    def test_question_representation(self):
        """
        The question's representation should return the question text.
        """
        question_text = "Sample question"
        question = create_question(question_text=question_text, days=0)
        self.assertEqual(repr(question), f"<Question: {question_text}>")
    
    def test_question_without_choices(self):
        """
        A question without choices should not be valid.
        """
        question_text = "No choices question"
        question = create_question(question_text=question_text, days=0)
        self.assertEqual(question.choice_set.count(), 0)

    def test_question_has_correct_number_of_choices(self):
        """
        A question should have the correct number of choices.
        """
        question_text = "Question with choices"
        question = create_question(question_text=question_text, days=0)
        choices = ["Choice 1", "Choice 2", "Choice 3"]
        for choice_text in choices:
            Choice.objects.create(question=question, choice_text=choice_text, votes=0)
        self.assertEqual(question.choice_set.count(), len(choices))

    def test_question_text_length(self):
        """
        The question text should not exceed 200 characters.
        """
        long_text = "x" * 201
        question = create_question(question_text=long_text, days=0)
        with self.assertRaises(ValidationError):
            question.full_clean()
            
    def test_default_vote_count(self):
        """
        The default vote count for choices should be zero.
        """
        question = create_question(question_text="Question with choice", days=0)
        choice = Choice.objects.create(question=question, choice_text="Choice 1")
        self.assertEqual(choice.votes, 0)
   
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose pub_date
        is in the future.
        """
        future_question = create_question(question_text="Future question.", days=5)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose pub_date
        is older than 1 day.
        """
        old_question = create_question(question_text="Old question.", days=-2)
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose pub_date
        is within the last day.
        """
        recent_question = create_question(question_text="Recent question.", days=-0.5)
        self.assertTrue(recent_question.was_published_recently())

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )
    
    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    
    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )
    
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionResultsViewTests(TestCase):
    def test_display_all_options(self):
        """
        The results view should display all the options for a question.
        """
        question = create_question(question_text="Question with options", days=0)
        choices = ["Option 1", "Option 2", "Option 3"]
        for choice_text in choices:
            Choice.objects.create(question=question, choice_text=choice_text, votes=0)
        url = reverse('polls:results', args=(question.id,))
        response = self.client.get(url)
        for choice_text in choices:
            self.assertContains(response, choice_text)
            
class VoteViewTests(TestCase):

    def test_vote_for_choice(self):
        """
        Voting for a choice increases its vote count.
        """
        question = create_question(question_text='Voting Question.', days=-1)
        choice = Choice.objects.create(question=question, choice_text='Choice 1')
        response = self.client.post(reverse('polls:vote', args=(question.id,)), {
            'choice': choice.id
        })
        self.assertRedirects(response, reverse('polls:results', args=(question.id,)))
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 1)

    def test_vote_for_no_choice(self):
        """
        Voting without selecting a choice should return an error message.
        """
        question = create_question(question_text='Voting Question.', days=-1)
        Choice.objects.create(question=question, choice_text='Choice 1')
        response = self.client.post(reverse('polls:vote', args=(question.id,)), {})
        self.assertContains(response, "You did not select a choice.")