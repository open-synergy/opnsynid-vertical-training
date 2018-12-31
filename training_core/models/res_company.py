# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    # Training Policy
    training_confirm_group_ids = fields.Many2many(
        string="Allowed Confirm Training",
        comodel_name="res.groups",
        relation="rel_company_training_allowed_confirm",
        column1="company_id",
        column2="group_id",
    )
    training_approve_group_ids = fields.Many2many(
        string="Allowed Approve Training",
        comodel_name="res.groups",
        relation="rel_company_training_allowed_approve",
        column1="company_id",
        column2="group_id",
    )
    training_start_group_ids = fields.Many2many(
        string="Allowed Start Training",
        comodel_name="res.groups",
        relation="rel_company_training_allowed_start",
        column1="company_id",
        column2="group_id",
    )
    training_finish_group_ids = fields.Many2many(
        string="Allowed Finish Training",
        comodel_name="res.groups",
        relation="rel_company_training_allowed_finish",
        column1="company_id",
        column2="group_id",
    )
    training_cancel_group_ids = fields.Many2many(
        string="Allowed Cancel Training",
        comodel_name="res.groups",
        relation="rel_company_training_allowed_cancel",
        column1="company_id",
        column2="group_id",
    )
    training_restart_group_ids = fields.Many2many(
        string="Allowed Restart Training",
        comodel_name="res.groups",
        relation="rel_company_training_allowed_restart",
        column1="company_id",
        column2="group_id",
    )

    # Training Participant
    training_participant_confirm_group_ids = fields.Many2many(
        string="Allowed Confirm Training Participant",
        comodel_name="res.groups",
        relation="rel_company_training_participant_allowed_confirm",
        column1="company_id",
        column2="group_id",
    )
    training_participant_approve_group_ids = fields.Many2many(
        string="Allowed Approve Training Participant",
        comodel_name="res.groups",
        relation="rel_company_training_participant_allowed_approve",
        column1="company_id",
        column2="group_id",
    )
    training_participant_pass_group_ids = fields.Many2many(
        string="Allowed Mark as Pass Training Participant",
        comodel_name="res.groups",
        relation="rel_company_training_participant_allowed_pass",
        column1="company_id",
        column2="group_id",
    )
    training_participant_fail_group_ids = fields.Many2many(
        string="Allowed Mark as Fail Training Participant",
        comodel_name="res.groups",
        relation="rel_company_training_participant_allowed_fail",
        column1="company_id",
        column2="group_id",
    )
    training_participant_cancel_group_ids = fields.Many2many(
        string="Allowed Cancel Training Participant",
        comodel_name="res.groups",
        relation="rel_company_training_participant_allowed_cancel",
        column1="company_id",
        column2="group_id",
    )
    training_participant_restart_group_ids = fields.Many2many(
        string="Allowed Restart Training Participant",
        comodel_name="res.groups",
        relation="rel_company_training_participant_allowed_restart",
        column1="company_id",
        column2="group_id",
    )
