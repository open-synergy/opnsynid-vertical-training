# -*- coding: utf-8 -*-
# Copyright 2009 Tech Receptives(<http://www.techreceptives.com>).
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class TrainingTrainer(models.Model):
    _name = "training.trainer"
    _descrption = "Faculty"
    _inherits = {
        "res.partner": "partner_id",
    }

    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
        ondelete="cascade",
    )
