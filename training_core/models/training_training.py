# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class TrainingTraining(models.Model):
    _name = "training.training"
    _inherit = ["mail.thread", "base.sequence_document",
                "base.workflow_policy_object"]
    _description = "Training"
    _order = "date_start desc, id"

    @api.multi
    @api.depends(
        "company_id",
    )
    def _compute_policy(self):
        _super = super(TrainingTraining, self)
        _super._compute_policy()

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    name = fields.Char(
        string="# Training Batch",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    source_document = fields.Char(
        string="Source Document",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    course_id = fields.Many2one(
        string="Course",
        comodel_name="training.course",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    participant_sequence_id = fields.Many2one(
        string="Participant Sequence",
        comodel_name="ir.sequence",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    method_ids = fields.Many2many(
        string="Methods",
        comodel_name="training.method",
        relation="rel_training_2_method",
        column1="training_id",
        column2="method_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_start = fields.Datetime(
        string="Date Start",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_end = fields.Datetime(
        string="Date End",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        copy=False,
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Approved"),
            ("start", "Started"),
            ("finish", "Finished"),
            ("cancel", "Cancelled"),
        ],
        required=True,
        default="draft",
    )
    cancel_reason_id = fields.Many2one(
        string="Cancel Reason",
        comodel_name="training.cancel_reason",
        copy=False,
    )
    note = fields.Text(
        string="Note",
    )
    trainer_ids = fields.Many2many(
        string="Trainer",
        comodel_name="training.trainer",
        relation="rel_training_2_trainer",
        column1="training_id",
        columns2="trainer_id",
        domain=[
            ("is_company", "=", False),
        ],
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    participant_ids = fields.One2many(
        string="Participants",
        comodel_name="training.training_participant",
        inverse_name="training_id",
        readonly=True,
        copy=False,
    )
    # Log Fields
    confirmed_date = fields.Datetime(
        string="Confirmation Date",
        readonly=True,
        copy=False,
    )
    confirmed_user_id = fields.Many2one(
        string="Confirmation By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    approved_date = fields.Datetime(
        string="Approved Date",
        readonly=True,
        copy=False,
    )
    approved_user_id = fields.Many2one(
        string="Approved By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    started_date = fields.Datetime(
        string="Started Date",
        readonly=True,
        copy=False,
    )
    started_user_id = fields.Many2one(
        string="Started By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    finished_date = fields.Datetime(
        string="Finished Date",
        readonly=True,
        copy=False,
    )
    finished_user_id = fields.Many2one(
        string="Finished By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancelled_date = fields.Datetime(
        string="Cancellation Date",
        readonly=True,
        copy=False,
    )
    cancelled_user_id = fields.Many2one(
        string="Cancellation By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    # Policy Fields
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    approve_ok = fields.Boolean(
        string="Can Approve",
        compute="_compute_policy",
    )
    start_ok = fields.Boolean(
        string="Can Start",
        compute="_compute_policy",
    )
    finish_ok = fields.Boolean(
        string="Can Finish",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )

    @api.multi
    def button_confirm(self):
        for training in self:
            training.write(training._prepare_confirm_data())

    @api.multi
    def button_approve(self):
        for training in self:
            training.write(training._prepare_approve_data())

    @api.multi
    def button_start(self):
        for training in self:
            training.write(training._prepare_start_data())

    @api.multi
    def button_finish(self):
        for training in self:
            training.write(training._prepare_finish_data())

    @api.multi
    def button_cancel(self, cancel_reason_id=False):
        for training in self:
            training.write(training._prepare_cancel_data(cancel_reason_id))

    @api.multi
    def button_restart(self):
        for training in self:
            training.write(training._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        result = {
            "state": "confirm",
            "confirmed_date": fields.Datetime.now(),
            "confirmed_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_approve_data(self):
        self.ensure_one()
        result = {
            "state": "approve",
            "approved_date": fields.Datetime.now(),
            "approved_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_start_data(self):
        self.ensure_one()
        result = {
            "state": "start",
            "started_date": fields.Datetime.now(),
            "started_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_finish_data(self):
        self.ensure_one()
        result = {
            "state": "finish",
            "finished_date": fields.Datetime.now(),
            "finished_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_cancel_data(self, cancel_reason_id=False):
        self.ensure_one()
        result = {
            "state": "cancel",
            "cancelled_date": fields.Datetime.now(),
            "cancelled_user_id": self.env.user.id,
            "cancel_reason_id": cancel_reason_id,
        }
        return result

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        result = {
            "state": "draft",
            "confirmed_date": False,
            "confirmed_user_id": False,
            "approved_date": False,
            "approved_user_id": False,
            "started_date": False,
            "started_user_id": False,
            "finished_date": False,
            "finished_user_id": False,
            "cancelled_date": False,
            "cancelled_user_id": False,
            "cancel_reason_id": False,
        }
        return result

    @api.model
    def create(self, values):
        _super = super(TrainingTraining, self)
        result = _super.create(values)
        result.write({
            "name": result._create_sequence(),
        })
        return result

    @api.constrains("date_start", "date_end")
    def _check_duration(self):
        strWarning = _("Date end must be greater than date start")
        if self.date_start and self.date_end:
            if self.date_end < self.date_start:
                raise UserError(strWarning)

    @api.multi
    def onchange_course_id(self, course_id):
        value = {}
        domain = {}
        return {"value": value, "domain": domain}

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for training in self:
            if training.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(TrainingTraining, self)
        _super.unlink()
