from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification


class NotificationSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='password123')
        self.receiver = User.objects.create_user(username='bob', password='password123')

    def test_notification_created_on_message(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hi Bob!")
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)

class MessageEditHistoryTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='Uchenna', password='password123')
        self.receiver = User.objects.create_user(username='Ikechukwu', password='password123')
        self.message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Original content")

    def test_message_edit_creates_history(self):
        # Edit the message
        self.message.content = "Updated content"
        self.message.save()

        # Check that history was created
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, "Original content")

        # Check that edited flag is set to True
        self.message.refresh_from_db()
        self.assertTrue(self.message.edited)