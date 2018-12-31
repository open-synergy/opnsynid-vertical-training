# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class TrainingClass(models.Model):
    _name = "training.class"
    _description = "Training Class"

    name = fields.Char(
        string="Method",
        required=True,
    )
    training_id = fields.Many2one(
        string="Training",
        comodel_name="training.training",
        required=True,
    )
    note = fields.Text(
        string="Note",
    )
