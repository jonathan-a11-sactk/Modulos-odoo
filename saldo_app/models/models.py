# -*- coding: utf-8 -*-
from odoo import models,fields,api
from odoo.exceptions import ValidationError


class Movimiento(models.Model):
    _name = 'sa.movimiento'
    _description = 'Movimientos'
    _inherit = 'mail.thread'

    name = fields.Char(string="Nombre de movimiento")
    type_movimiento = fields.Selection(selection=[("ingreso","Ingreso"),("gasto","Gasto")],default="ingreso",required=True)
    date = fields.Date(string="Fecha del movimiento")
    amount = fields.Float(string="Monto del movimiento", track_visibility="onchange")
    receipt_name = fields.Binary(string="Foto del recibo")
    res_user_id = fields.Many2one ('res.users', string="Usuarios",default= lambda self:self.env.user.id)
    notas = fields.Html(string="Notas de movimiento")
    currency_id = fields.Many2one('res.currency', string="Moneda")
    tag_ids = fields.Many2many("sa.tag","sa_move_sa_tag_rel","move_id","tag_id")
    category_id = fields.Many2one('sa.category', string="Categoria")
    email = fields.Char(related ="res_user_id.email", string="Email usuario")

    @api.constrains("amount")
    def check_amount(self):
        if not(self.amount>=0 and self.amount<=100000):
            raise ValidationError("El valor ingreso no puede ya que no esta en el intervalo permitido")

    def create(self,vals):
        nombre = vals.get("name","-")
        tipo_movimiento = vals.get("type_movimiento","-")
        date = vals.get("date","-")
        amount = vals.get("amount","-")
        notas = "el nombre del movimiento{} el tipo de movimiento es {} y la fecha del movimiento es {}"
        vals["notas"]=notas.format(nombre,tipo_movimiento,date,amount)
        return super(Movimiento,self).create(vals)

class Category(models.Model):
    _name = "sa.category"
    _description = "Category"

    name = fields.Char(string="Nombre de la categoria")

    def ver_movimiento(self):
        return {
            "type": "ir.actions.act_window",
            "name": "EL movimiento" + self.name,
            "res_model": "sa.movimiento",
            "target": "new",
            "views": [[False, "tree"]],
            "domain": [["category_id", "=", self.id]]
        }


class Tag(models.Model):
    _name = "sa.tag"
    _description = "Tag"

class ResUsers(models.Model):
    _inherit = "res.users"
    _description ="Usuarios"

    movimientos_ids = fields.One2many("sa.movimiento","res_user_id")
    movimientos_ingresos = fields.Char(string="Movimientos ingresos", compute="calcular_movimientos")
    movmientos_gastos = fields.Char(string="Movimientos gastos",compute="calcular_movimientos")

    @api.depends("movimientos_ids")
    def calcular_movimientos(self):
        for record in self:
            record.movimientos_ingresos = sum(record.movimientos_ids.filtered(lambda r:r.type_movimiento == "ingreso").mapped("amount"))
            record.movmientos_gastos = sum(record.movimientos_ids.filtered(lambda r:r.type_movimiento== "gasto").mapped("amount"))

    def menu_root(self):
        return{
            "type":"ir.actions.act_window",
            "name":"Menu para usuario",
            "res_model":"res.users",
            "target":"self",
            "views":[(False,"form")],
            "res_id":self.env.user.id
        }

