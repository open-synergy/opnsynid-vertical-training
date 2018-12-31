# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields


class TrainingCancelParticipant(models.TransientModel):
    _name = "training.cancel_participant"
    _description = "Cancel Participant"

    cancel_reason_id = fields.Many2one(
        string="Cancel Reason",
        comodel_name="training.participant_cancel_reason",
        required=True,
    )

    @api.multi
    def action_confirm(self):
        for wiz in self:
            wiz._confirm_cancel()

    @api.multi
    def _confirm_cancel(self):
        self.ensure_one()
        participant_ids = self.env.context.get("active_ids", [])
        participants = self.env["training.training_participant"].browse(
            participant_ids
        )
        participants.button_cancel(self.cancel_reason_id.id)
