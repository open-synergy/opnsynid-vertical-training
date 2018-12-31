# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class TrainingCourse(models.Model):
    _name = "training.course"
    _description = "Training Category"

    code = fields.Char(
        string="Code",
        required=True,
    )
    name = fields.Char(
        string="Training Course",
        required=True,
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    training_confirm_group_ids = fields.Many2many(
        string="Allow To Confirm Training",
        comodel_name="res.groups",
        relation="rel_allowed_confirm_training",
        column1="course_id",
        column2="group_id",
    )
    training_approve_group_ids = fields.Many2many(
        string="Allow To Approve Training",
        comodel_name="res.groups",
        relation="rel_allowed_approve_training",
        column1="course_id",
        column2="group_id",
    )
    training_start_group_ids = fields.Many2many(
        string="Allow To Start Training",
        comodel_name="res.groups",
        relation="rel_allowed_start_training",
        column1="course_id",
        column2="group_id",
    )
    training_finish_group_ids = fields.Many2many(
        string="Allow To Finish Training",
        comodel_name="res.groups",
        relation="rel_allowed_finish_training",
        column1="course_id",
        column2="group_id",
    )
    training_cancel_group_ids = fields.Many2many(
        string="Allow To Cancel Training",
        comodel_name="res.groups",
        relation="rel_allowed_cancel_training",
        column1="course_id",
        column2="group_id",
    )
    training_restart_group_ids = fields.Many2many(
        string="Allow To Restart Training",
        comodel_name="res.groups",
        relation="rel_allowed_restart_training",
        column1="course_id",
        column2="group_id",
    )
