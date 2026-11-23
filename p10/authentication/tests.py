"""Tests for user accounts."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import User
from projects.models import Comment, Contributor, Issue, Project


class AccountDeletionTests(APITestCase):
    """RGPD: deleting an account erases the user, anonymizes their content.

    Alice owns a project where Bob contributes: each one has an issue and
    comments on the other's issue, and Alice's issue is assigned to Bob.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        """Build Alice's project with Bob's and Alice's crossed contributions."""
        cls.alice = User.objects.create_user(
            username="alice", password="unused", age=30
        )
        cls.bob = User.objects.create_user(username="bob", password="unused", age=30)

        cls.project = Project.objects.create(
            author=cls.alice, name="Projet", description="d"
        )
        Contributor.objects.create(user=cls.alice, project=cls.project)
        Contributor.objects.create(user=cls.bob, project=cls.project)

        cls.alice_issue = Issue.objects.create(
            author=cls.alice,
            project=cls.project,
            name="Issue d'Alice",
            description="d",
            assigned_to=cls.bob,
        )
        cls.bob_issue = Issue.objects.create(
            author=cls.bob,
            project=cls.project,
            name="Issue de Bob",
            description="d",
        )

        cls.bob_comment_on_alice_issue = Comment.objects.create(
            author=cls.bob, issue=cls.alice_issue, description="d"
        )
        cls.alice_comment_on_bob_issue = Comment.objects.create(
            author=cls.alice, issue=cls.bob_issue, description="d"
        )

    def delete_account(self, user: User) -> None:
        """Delete the user's own account through the API."""
        self.client.force_authenticate(user=user)
        response = self.client.delete(reverse("user-detail", args=[user.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def assert_anonymized(self, *objects: Project | Issue | Comment) -> None:
        """Each object still exists, detached from its deleted author."""
        for obj in objects:
            obj.refresh_from_db()
            self.assertIsNone(obj.author)

    def test_project_author_deletion_anonymizes_her_content(self) -> None:
        """Alice's account goes away; her content stays anonymized, Bob's is intact."""
        self.delete_account(self.alice)

        self.assertFalse(User.objects.filter(pk=self.alice.pk).exists())
        self.assertFalse(Contributor.objects.filter(user_id=self.alice.pk).exists())
        self.assert_anonymized(
            self.project, self.alice_issue, self.alice_comment_on_bob_issue
        )

        self.bob_issue.refresh_from_db()
        self.bob_comment_on_alice_issue.refresh_from_db()
        self.assertEqual(self.bob_issue.author, self.bob)
        self.assertEqual(self.bob_comment_on_alice_issue.author, self.bob)
        self.assertTrue(
            Contributor.objects.filter(user=self.bob, project=self.project).exists()
        )

    def test_contributor_deletion_anonymizes_his_content(self) -> None:
        """Bob's account goes away; his content stays anonymized, Alice's is intact."""
        self.delete_account(self.bob)

        self.assertFalse(User.objects.filter(pk=self.bob.pk).exists())
        self.assertFalse(Contributor.objects.filter(user_id=self.bob.pk).exists())
        self.assert_anonymized(self.bob_issue, self.bob_comment_on_alice_issue)

        self.alice_comment_on_bob_issue.refresh_from_db()
        self.assertEqual(self.alice_comment_on_bob_issue.author, self.alice)
        self.alice_issue.refresh_from_db()
        self.assertIsNone(self.alice_issue.assigned_to)

    def test_anonymized_content_is_read_only(self) -> None:
        """Nobody becomes author of an orphaned issue: Alice cannot edit Bob's."""
        self.delete_account(self.bob)

        self.client.force_authenticate(user=self.alice)
        url = reverse("project-issue-detail", args=[self.project.pk, self.bob_issue.pk])
        response = self.client.patch(url, {"name": "repris"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["author"])

    def test_cannot_delete_another_account(self) -> None:
        """Bob cannot delete Alice's account: 404, nothing is erased."""
        self.client.force_authenticate(user=self.bob)
        response = self.client.delete(reverse("user-detail", args=[self.alice.pk]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(User.objects.filter(pk=self.alice.pk).exists())
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())
