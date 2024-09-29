# -*- coding: utf-8 -*-

import base64
import logging
import json

from odoo import models, fields

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    website_status = fields.Boolean(string='Publish on website')
    
    def action_refresh_data_model(self, list_record):
        conector_id = self.env['connector.base'].search([('type_app', '=', 'odoo')])
        line_id = conector_id.connector_model_ids.filtered(lambda m: m.model_id.model==self._name)
        values = line_id._action_record_values('get_value_product', list_record)
        return values

    def create_or_update_attachment(self, vals):
        obj_attachment = self.env['ir.attachment']
        result = vals[self.id]['result']
        try:
            attachment_vals = {
                'datas': base64.b64encode(json.dumps(result, indent=4).encode('utf-8'))
            }
            domain = [('res_model', '=', 'product.template'), ('res_id', '=', self.id)]
            attachment_id = obj_attachment.search(domain)
            if attachment_id:
                attachment_id.write(attachment_vals)
            else:
                attachment_vals.update({
                    'name': f'{self.default_code} .json',
                    'res_model': 'product.template',
                    'res_id': self.id,
                })
                attachment_id = obj_attachment.create(attachment_vals)
        except Exception as e:
            _logger.error(f"Error in create_or_update_attachment: {e}")
        return result
            
    def create_record_product(self):
        obj_attachment = self.env['ir.attachment']
        product_data = {
            'res_model': 'product.template',
            'res_id': self.id,
            'product_tag_ids.name': self.product_tag_ids.name,
            'detailed_type': self.detailed_type,
            'categ_id': self.categ_id.name,
            'default_code': self.default_code,
            'barcode': self.barcode,
        }
        product_json = json.dumps(product_data, indent=4)
        product_record = {
            'datas': base64.b64encode(product_json.encode('utf-8')),
        }
        attachment_id = obj_attachment.search([
            ('res_model', '=', 'product.template'),
            ('res_id', '=', self.id)
        ])
        if attachment_id:
            attachment_id.write(product_record)
        else:
            product_record.update({
                'name': f'{self.default_code}.json',
                'res_model': 'product.template',
                'res_id': self.id,   
            })
            attachment_id = obj_attachment.create(product_record)
        return product_record
