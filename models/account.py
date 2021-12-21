from odoo import fields, models,api,_

from uuid import uuid4
import qrcode
import base64
import logging

from lxml import etree



class AccountMove(models.Model):
    _inherit = "account.move"


    def _ubl_add_attachments(self, parent_node, ns, version="2.1"):
        self.ensure_one()
        self.billing_refence(parent_node, ns, version="2.1")
        # if self.decoded_data:
        self.testing()
        self.qr_code(parent_node, ns, version="2.1")
        self.qr_1code(parent_node, ns, version="2.1")
        self.pih_code(parent_node, ns, version="2.1")

        # self.signature_refence(parent_node, ns, version="2.1")
        # if self.company_id.embed_pdf_in_ubl_xml_invoice and not self.env.context.get(
        #     "no_embedded_pdf"
        # ):
        # self.signature_refence(parent_node, ns, version="2.1")
        filename = "Invoice-" + self.name + ".pdf"
        docu_reference = etree.SubElement(
            parent_node, ns["cac"] + "AdditionalDocumentReference"
        )
        docu_reference_id = etree.SubElement(docu_reference, ns["cbc"] + "ID")
        docu_reference_id.text = filename
        attach_node = etree.SubElement(docu_reference, ns["cac"] + "Attachment")
        binary_node = etree.SubElement(
            attach_node,
            ns["cbc"] + "EmbeddedDocumentBinaryObject",
            mimeCode="application/pdf",
            filename=filename,
        )
        ctx = dict()
        ctx["no_embedded_ubl_xml"] = True
        ctx["force_report_rendering"] = True
        # pdf_inv = (
        #     self.with_context(ctx)
        #     .env.ref("account.account_invoices")
        #     ._render_qweb_pdf(self.ids)[0]
        # )
        ########changed########################
        pdf_inv = self.with_context(ctx).env.ref(
            'account_invoice_ubl.account_invoices_1')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
            'account_invoice_ubl.account_invoices_b2b')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
            'account_invoice_ubl.account_invoices_b2b_credit')._render_qweb_pdf(self.ids)[0]
        # pdf_inv = self.with_context(ctx).env.ref(
        #     'account_invoice_ubl.account_invoices_b2b_debit')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
            'account_invoice_ubl.account_invoices_b2c')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
                    'account_invoice_ubl.account_invoices_b2c_credit')._render_qweb_pdf(self.ids)[0]
        # +++++++++++++++++++++++++++++++OUR CUSTOMES ADD HERE+++++++++++++++++++++++++++++++++++++
        # pdf_inv = self.with_context(ctx).env.ref(
        #     'tam.tam_invoice_report')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
            'tam.tamhub_invoice_report')._render_qweb_pdf(self.ids)[0]
        pdf_inv = self.with_context(ctx).env.ref(
            'tam_2nd_invoice.tamhub_invoice_report_second')._render_qweb_pdf(self.ids)[0]

       # -----------------------------aboveeeeeeee---------------------------------

        binary_node.text = base64.b64encode(pdf_inv)
        # self.qr3_code(parent_node, ns, version="2.1")


        # filename = "ICV"
        # icv_reference = etree.SubElement(
        #     parent_node, ns["cac"] + "AdditionalDocumentReference"
        # )
        # icv_reference_id = etree.SubElement(icv_reference, ns["cbc"] + "ID")
        # icv_reference_id.text = filename
        # icv_reference_node = etree.SubElement(icv_reference, ns["cac"] + "UUID")
        # icv_reference_node.text = self.name

    @api.model
    def _get_invoice_report_names(self):
        return [
            "account.report_invoice",
            "account.report_invoice_with_payments",
            "account_invoice_ubl.report_invoice_1",
            "account_invoice_ubl.report_invoice_b2b",
            "account_invoice_ubl.report_invoice_b2b_credit",
            # "account_invoice_ubl.report_invoice_b2b_debit",
            "account_invoice_ubl.report_invoice_b2c",
            "account_invoice_ubl.report_invoice_b2c_credit",
            # "account_invoice_ubl.report_invoice_b2c_debit",
            # "tam.invoice_format_view2",
            "tam.tamhub_invoice_view",
            "tam_2nd_invoice.tamhub_invoice_view_second",

        ]
class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"


    @classmethod
    def _get_invoice_reports_ubl(cls):
        return [
            "account.report_invoice",
            'account_invoice_ubl.report_invoice_1',
            'account_invoice_ubl.report_invoice_b2b',
            'account_invoice_ubl.report_invoice_b2b_credit',
            'account_invoice_ubl.report_invoice_b2b_debit',
            'account_invoice_ubl.report_invoice_b2c',
            'account_invoice_ubl.report_invoice_b2c_credit',
            'account_invoice_ubl.report_invoice_b2c_debit',
            "account.report_invoice_with_payments",
            "account.account_invoice_report_duplicate_main",
            # "tam.invoice_format_view2",
            "tam.tamhub_invoice_view",
            "tam_2nd_invoice.tamhub_invoice_view_second",
        ]






