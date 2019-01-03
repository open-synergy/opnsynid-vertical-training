# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Training Verticalization - Fee",
    "version": "8.0.1.1.0",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "training_core",
        "account_accountant",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/create_invoice.xml",
        "views/training_course_views.xml",
        "views/training_training_views.xml",
        "views/training_training_participant_views.xml",
    ],
}
