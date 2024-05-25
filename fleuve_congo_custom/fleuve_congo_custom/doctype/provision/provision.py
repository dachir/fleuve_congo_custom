# Copyright (c) 2024, Kossivi Amouzou and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Provision(Document):

	def get_provision_ratio(self, employee, table):
		return frappe.db.sql(
			"""
			SELECT r.*
			FROM tabProvision p INNER JOIN {tbl} r ON p.name = r.parent
			WHERE r.employee = %(employee)s AND YEAR(p.end_date) = %(fiscal_year)s
			""".format( tbl=table ), 
			{"fiscal_year":int(self.fiscal_year) - 1, "employee": employee}, as_dict=1
		)


	def get_provision_details(self, employee=None):
		employee_name = employee if employee else "%"
		return frappe.db.sql(
			"""
			SELECT y.*,
			y.salaire01 / y.ratio_total * y.ratio01 AS `gratif01`,
			y.salaire02 / y.ratio_total * y.ratio02 AS `gratif02`,
			y.salaire03 / y.ratio_total * y.ratio03 AS `gratif03`,
			y.salaire04 / y.ratio_total * y.ratio04 AS `gratif04`,
			y.salaire05 / y.ratio_total * y.ratio05 AS `gratif05`,
			y.salaire06 / y.ratio_total * y.ratio06 AS `gratif06`,
			y.salaire07 / y.ratio_total * y.ratio07 AS `gratif07`,
			y.salaire08 / y.ratio_total * y.ratio08 AS `gratif08`,
			y.salaire09 / y.ratio_total * y.ratio09 AS `gratif09`,
			y.salaire10 / y.ratio_total * y.ratio10 AS `gratif10`,
			y.salaire11 / y.ratio_total * y.ratio11 AS `gratif11`,
			y.salaire12 / y.ratio_total * y.ratio12 AS `gratif12`,

			y.salaire01 / 26 * y.ratio01 AS `salmois01`,
			y.salaire02 / 26 * y.ratio02 AS `salmois02`,
			y.salaire03 / 26 * y.ratio03 AS `salmois03`,
			y.salaire04 / 26 * y.ratio04 AS `salmois04`,
			y.salaire05 / 26 * y.ratio05 AS `salmois05`,
			y.salaire06 / 26 * y.ratio06 AS `salmois06`,
			y.salaire07 / 26 * y.ratio07 AS `salmois07`,
			y.salaire08 / 26 * y.ratio08 AS `salmois08`,
			y.salaire09 / 26 * y.ratio09 AS `salmois09`,
			y.salaire10 / 26 * y.ratio10 AS `salmois10`,
			y.salaire11 / 26 * y.ratio11 AS `salmois11`,
			y.salaire12 / 26 * y.ratio12 AS `salmois12`
			FROM
				(SELECT w.*,  
				ratio01 + ratio02 + ratio03 + ratio04 + ratio05 + ratio06 + ratio07 + ratio08 + ratio09 + ratio10 + ratio11 + ratio12 AS ratio_total
				FROM(
					SELECT v.employee,
					SUM(CASE WHEN v.mois = 1 THEN new_rate ELSE 0 END) AS `ratio01`,
					SUM(CASE WHEN v.mois = 2 THEN new_rate ELSE 0 END) AS `ratio02`,
					SUM(CASE WHEN v.mois = 3 THEN new_rate ELSE 0 END) AS `ratio03`,
					SUM(CASE WHEN v.mois = 4 THEN new_rate ELSE 0 END) AS `ratio04`,
					SUM(CASE WHEN v.mois = 5 THEN new_rate ELSE 0 END) AS `ratio05`,
					SUM(CASE WHEN v.mois = 6 THEN new_rate ELSE 0 END) AS `ratio06`,
					SUM(CASE WHEN v.mois = 7 THEN new_rate ELSE 0 END) AS `ratio07`,
					SUM(CASE WHEN v.mois = 8 THEN new_rate ELSE 0 END) AS `ratio08`,
					SUM(CASE WHEN v.mois = 9 THEN new_rate ELSE 0 END) AS `ratio09`,
					SUM(CASE WHEN v.mois = 10 THEN new_rate ELSE 0 END) AS `ratio10`,
					SUM(CASE WHEN v.mois = 11 THEN new_rate ELSE 0 END) AS `ratio11`,
					SUM(CASE WHEN v.mois = 12 THEN new_rate ELSE 0 END) AS `ratio12`,
					
					SUM(CASE WHEN v.mois = 1 THEN salaire ELSE 0 END) AS `salaire01`,
					SUM(CASE WHEN v.mois = 2 THEN salaire ELSE 0 END) AS `salaire02`,
					SUM(CASE WHEN v.mois = 3 THEN salaire ELSE 0 END) AS `salaire03`,
					SUM(CASE WHEN v.mois = 4 THEN salaire ELSE 0 END) AS `salaire04`,
					SUM(CASE WHEN v.mois = 5 THEN salaire ELSE 0 END) AS `salaire05`,
					SUM(CASE WHEN v.mois = 6 THEN salaire ELSE 0 END) AS `salaire06`,
					SUM(CASE WHEN v.mois = 7 THEN salaire ELSE 0 END) AS `salaire07`,
					SUM(CASE WHEN v.mois = 8 THEN salaire ELSE 0 END) AS `salaire08`,
					SUM(CASE WHEN v.mois = 9 THEN salaire ELSE 0 END) AS `salaire09`,
					SUM(CASE WHEN v.mois = 10 THEN salaire ELSE 0 END) AS `salaire10`,
					SUM(CASE WHEN v.mois = 11 THEN salaire ELSE 0 END) AS `salaire11`,
					SUM(CASE WHEN v.mois = 12 THEN salaire ELSE 0 END) AS `salaire12`
					
					FROM
						(SELECT t.annee, t.mois, t.date_begin, t.date_end, t.date_join, t.date_debut, t.date_fin, t.date_quit, t.employee,
											(t.start_period_day / t.period_day * t.rate) + t.years_div_5 AS new_rate, 
											t.period_day, t.rate, t.salaire, t.start_period_day, t.years_difference, t.years_div_5, t.categorie
										FROM (
											SELECT 
												e.name as employee, 
												YEAR(p.end_date) AS annee, 
												MONTH(p.end_date) AS mois,
												CASE 
													WHEN p.end_date >= e.date_of_joining THEN  
														CASE 
															WHEN e.relieving_date IS NULL THEN 1.5
															WHEN e.relieving_date > p.start_date THEN 1.5 
															ELSE 0 
														END
													ELSE 0 
												END AS rate,
												DATEDIFF(p.end_date, p.start_date) AS period_day,
												CASE 
													WHEN STR_TO_DATE(CONCAT(YEAR(p.end_date), '-', MONTH(e.date_of_joining), '-', DAY(e.date_of_joining)), '%%Y-%%m-%%d') BETWEEN p.start_date AND p.end_date THEN
														CASE 
															WHEN YEAR(p.end_date) = YEAR(e.date_of_joining) THEN
																DATEDIFF(p.end_date, STR_TO_DATE(CONCAT(YEAR(p.end_date), '-', MONTH(e.date_of_joining), '-', DAY(e.date_of_joining)), '%%Y-%%m-%%d')) + 1 
															ELSE
																DATEDIFF(p.end_date, p.start_date)
														END
													ELSE 
														DATEDIFF(p.end_date, p.start_date)
												END AS start_period_day,
												e.relieving_date AS date_quit,
												p.end_date AS date_end, 
												p.start_date AS date_begin, 
												e.date_of_joining AS date_join,
												TIMESTAMPDIFF(YEAR, e.date_of_joining, p.end_date) AS years_difference,
												CASE 
													WHEN STR_TO_DATE(CONCAT(YEAR(p.end_date), '-', MONTH(e.date_of_joining), '-', DAY(e.date_of_joining)), '%%Y-%%m-%%d') BETWEEN p.start_date AND p.end_date
														AND (e.relieving_date > p.start_date OR e.relieving_date IS NULL) THEN
														TIMESTAMPDIFF(YEAR, e.date_of_joining, p.end_date) DIV 5 
													ELSE 0
												END AS years_div_5,
												se.categorie, se.date_debut, se.salaire, IFNULL(se.date_fin, DATE_FORMAT(NOW(),'%%Y-12-31'))  AS date_fin
											FROM 
												tabEmployee e 
												CROSS JOIN `tabPayroll Period` p INNER JOIN `tabSalaire employee` se ON e.name = se.parent 
											WHERE 
												YEAR(p.end_date) = %(fiscal_year)s AND e.name LIKE %(employee)s
										) AS t  
										WHERE t.date_begin BETWEEN t.date_debut AND t.date_fin 
						) v
						GROUP BY v.employee) AS w) AS y 
			""", {"fiscal_year":self.fiscal_year, "employee": employee_name}, as_dict=1
		)

	@frappe.whitelist()
	def add_details(self):
		self.ratio.clear()
		self.conge.clear()
		self.gratification.clear()

		liste = self.get_provision_details()
		
		for i in liste:
			ly_total_ratio = 0
			ly_total_conge = 0
			ly_total_gratif = 0

			details = self.get_provision_ratio(i.employee, '`tabProvision Ratio`')
			if details:
				if details[0]:
					ly_total_ratio = details[0].total if details[0].total else 0

			details = self.get_provision_ratio(i.employee, '`tabProvision Conge`')
			if details:
				if details[0]:
					ly_total_conge = details[0].total if details[0].total else 0

			details = self.get_provision_ratio(i.employee, '`tabProvision Gratification`')
			if details:
				if details[0]:
					ly_total_gratif = details[0].total if details[0].total else 0

			self.append(
					"ratio",
					{
						"employee": i.employee,
						"report": ly_total_ratio,
						"janvier": i.ratio01,
						"fevrier": i.ratio02,
						"mars": i.ratio03,
						"avril": i.ratio04,
						"mai": i.ratio05,
						"juin": i.ratio06,
						"juillet": i.ratio07,
						"aout": i.ratio08,
						"septembre": i.ratio09,
						"octobre": i.ratio10,
						"novembre": i.ratio11,
						"decembre": i.ratio12,
						"total": i.ratio_total + ly_total_ratio,
					}
				)

			self.append(
					"conge",
					{
						"employee": i.employee,
						"report": ly_total_conge,
						"janvier": i.salmois01,
						"fevrier": i.salmois02,
						"mars": i.salmois03,
						"avril": i.salmois04,
						"mai": i.salmois05,
						"juin": i.salmois06,
						"juillet": i.salmois07,
						"aout": i.salmois08,
						"septembre": i.salmois09,
						"octobre": i.salmois10,
						"novembre": i.salmois11,
						"decembre": i.salmois12,
						"total": ly_total_conge + i.salmois01 + i.salmois02 + i.salmois03 + i.salmois04 + i.salmois05 + i.salmois06 + i.salmois07 + i.salmois08 + i.salmois09 + i.salmois10 + i.salmois11 + i.salmois12
					}
				)

			self.append(
					"gratification",
					{
						"employee": i.employee,
						"report": ly_total_gratif,
						"janvier": i.gratif01,
						"fevrier": i.gratif02,
						"mars": i.gratif03,
						"avril": i.gratif04,
						"mai": i.gratif05,
						"juin": i.gratif06,
						"juillet": i.gratif07,
						"aout": i.gratif08,
						"septembre": i.gratif09,
						"octobre": i.gratif10,
						"novembre": i.gratif11,
						"decembre": i.gratif12,
						"total": ly_total_gratif + i.gratif01 + i.gratif02 + i.gratif03 + i.gratif04 + i.gratif05 + i.gratif06 + i.gratif07 + i.gratif08 + i.gratif09 + i.gratif10 + i.gratif11 + i.gratif12 
					}
				)

	def before_save(self):
		self.add_details()
				


