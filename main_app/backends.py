from organizations.backends.defaults import InvitationBackend


class CustomInvitations(InvitationBackend):
    def invite_by_email(self, email, sender=None, request=None, **kwargs):
      try:
          user = self.user_model.objects.get(email=email)
      except self.user_model.DoesNotExist:
          user = self.user_model.objects.create(email=email,
                  password=self.user_model.objects.make_random_password())
          user.is_active = False
          user.save()
      self.send_invitation(user, sender, **kwargs)
      return user