# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Training Verticalization - Core",
    "version": "8.0.1.0.0",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "document",
        "base_location_lau_level3",
        "partner_identification",
        "partner_emergency_contact",
        "partner_experience",
        "partner_contact_gender",
        "partner_contact_nationality",
        "partner_contact_blood_type",
        "partner_place_of_birth",
        "partner_contact_birthdate",
        "partner_contact_religion",
        "partner_contact_ethnicity",
        "partner_contact_family",
        "base_sequence_configurator",
        "base_workflow_policy",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "menu.xml",
        "wizards/cancel_participant.xml",
        "wizards/cancel_training.xml",
        "views/training_config_setting_views.xml",
        "views/training_course_views.xml",
        "views/training_method_views.xml",
        "views/training_class_views.xml",
        "views/training_cancel_reason_views.xml",
        "views/training_participant_cancel_reason_views.xml",
        "views/training_training_views.xml",
        "views/training_participant_views.xml",
        "views/training_training_participant_views.xml",
        "views/training_trainer_views.xml",
    ],
}
