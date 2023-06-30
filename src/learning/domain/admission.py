from datetime import datetime


class Admission():
    def __init__(self, user, course, squad, is_premium, paid_at):
        self.user = user
        self.course = course
        self.squad = squad
        self.is_premium = is_premium
        self.paid_at = paid_at

    def grant_premium(self, squad_id):
        self.squad_id = squad_id
        self.paid_at = datetime.now()
        self.is_premium = True

    def revoke_premium(self):
        self.is_premium = False
        self.paid_at = None
        self.squad = None
