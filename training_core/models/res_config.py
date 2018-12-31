# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ResConfig(models.TransientModel):
    _name = "training.config_setting"
    _inherit = "res.config.settings"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    training_confirm_group_ids = fields.Many2many(
        string="Allowed Confirm Training",
        comodel_name="res.groups",
        related="company_id.training_confirm_group_ids",
    )
    training_approve_group_ids = fields.Many2many(
        string="Allowed Approve Training",
        comodel_name="res.groups",
        related="company_id.training_approve_group_ids",
    )
    training_start_group_ids = fields.Many2many(
        string="Allowed Start Training",
        comodel_name="res.groups",
        related="company_id.training_start_group_ids",
    )
    training_finish_group_ids = fields.Many2many(
        string="Allowed Finish Training",
        comodel_name="res.groups",
        related="company_id.training_finish_group_ids",
    )
    training_cancel_group_ids = fields.Many2many(
        string="Allowed Cancel Training",
        comodel_name="res.groups",
        related="company_id.training_cancel_group_ids",
    )
    training_restart_group_ids = fields.Many2many(
        string="Allowed Restart Training",
        comodel_name="res.groups",
        related="company_id.training_restart_group_ids",
    )

    training_participant_confirm_group_ids = fields.Many2many(
        string="Allowed Confirm Training Participant",
        comodel_name="res.groups",
        related="company_id.training_participant_confirm_group_ids",
    )
    training_participant_approve_group_ids = fields.Many2many(
        string="Allowed Approve Training Participant",
        comodel_name="res.groups",
        related="company_id.training_participant_approve_group_ids",
    )
    training_participant_pass_group_ids = fields.Many2many(
        string="Allowed Mark as Pass Training Participant",
        comodel_name="res.groups",
        related="company_id.training_participant_pass_group_ids",
    )
    training_participant_fail_group_ids = fields.Many2many(
        string="Allowed Mark as Fail Training Participant",
        comodel_name="res.groups",
        related="company_id.training_participant_fail_group_ids",
    )
    training_participant_cancel_group_ids = fields.Many2many(
        string="Allowed Cancel Training Participant",
        comodel_name="res.groups",
        related="company_id.training_participant_cancel_group_ids",
    )
    training_participant_restart_group_ids = fields.Many2many(
        string="Allowed Restart Training Participant",
        comodel_name="res.groups",
        related="company_id.training_participant_restart_group_ids"
    )
