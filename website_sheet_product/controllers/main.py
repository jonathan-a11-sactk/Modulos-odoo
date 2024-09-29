# -*- coding: utf-8 -*-

import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class WebsiteSheetProduct(http.Controller):

    @http.route('/website_sheet_product/page1', auth='public', website=True)
    def page1(self,search=None, **kw):
        obj_product = request.env['product.template']
        domain = [('website_status', '=', True)]
        if search:
            domain += ['|', ('default_code', 'ilike', search), ('name', 'ilike', search)]
        products = obj_product.search(domain)  
        return request.render('website_sheet_product.page1', {'products': products,'search_term': search})

    @http.route('/website_sheet_product/page2/<int:product_id>', auth='public', website=True)
    def page2(self, product_id, **kw):
        product_id = request.env['product.template'].browse(product_id)
        list_record = {}
        if product_id.id not in list_record:
            list_record[product_id.id] = {
                'domain': [('default_code', '=', product_id.default_code)],
                'vals': {}, 
                'errores': [],
                'ids': product_id.id_odoo,
            }                
        results = product_id.action_refresh_data_model(list_record)
        vals, result, errores = results.get(product_id.id).values()
        if len(errores):
            _logger.error(','.join(errores))
        iqc_lm_dict = {}
        for line_bom in result.get('list_boms', []):
            for line_product in line_bom.get('list_products', []):
                for key, value in line_product.get('product_qc').items():
                    if int(key) not in iqc_lm_dict:
                        iqc_lm_dict[int(key)] = value
        request.session['list_boms'] = iqc_lm_dict
        return request.render('website_sheet_product.page2', {'product': product_id, 'list_record': result})
    
    @http.route('/website_sheet_product/page3/<int:product_id>', auth='public', website=True)
    def page3(self, product_id, **kw):
        list_boms = request.session.get('list_boms', {})
        vals = list_boms.get(product_id)
        return request.render('website_sheet_product.page3', {'bom_quality_list': vals})
