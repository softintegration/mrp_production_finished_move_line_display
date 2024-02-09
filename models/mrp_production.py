# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, Command, fields, models, _
from odoo.osv import expression
from odoo.tools import float_compare, float_round, float_is_zero, OrderedSet


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    finished_move_line_ids_count = fields.Integer(compute='_compute_finished_move_line_ids_count')

    @api.depends('finished_move_line_ids')
    def _compute_finished_move_line_ids_count(self):
        for each in self:
            each.finished_move_line_ids_count = len(each.finished_move_line_ids)

    def show_finished_move_line_ids(self):
        self.ensure_one()
        domain = [('id', 'in', self.move_finished_ids.mapped('move_line_ids').ids)]
        return {
            'name': _('Finished Product'),
            'view_mode': 'tree,form',
            'views': [(self.env.ref('stock.view_move_line_tree').id, 'tree'),
                      (self.env.ref('stock.view_move_line_form').id, 'form')],
            'res_model': 'stock.move.line',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
        }