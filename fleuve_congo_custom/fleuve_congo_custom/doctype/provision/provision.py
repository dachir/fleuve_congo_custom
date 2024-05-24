# Copyright (c) 2024, Kossivi Amouzou and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Provision(Document):

	@frappe.whitelist()
	def add_details(self):
		#result = frappe.db.sql("""SELECT COUNT(*) as nb  FROM tabEmployee""", as_dict=1)
		#e = len(str(result[0].nb))
		#cpt = self.fiscal_year * 10**e
		self.ratio.clear()

		if not self.ratio:
			liste = frappe.db.sql(
				"""
				SELECT y.*,
				y.salaire01 / y.ratio_total * y.ratio01 AS `13mois01`,
				y.salaire02 / y.ratio_total * y.ratio02 AS `13mois02`,
				y.salaire03 / y.ratio_total * y.ratio03 AS `13mois03`,
				y.salaire04 / y.ratio_total * y.ratio04 AS `13mois04`,
				y.salaire05 / y.ratio_total * y.ratio05 AS `13mois05`,
				y.salaire06 / y.ratio_total * y.ratio06 AS `13mois06`,
				y.salaire07 / y.ratio_total * y.ratio07 AS `13mois07`,
				y.salaire08 / y.ratio_total * y.ratio08 AS `13mois08`,
				y.salaire09 / y.ratio_total * y.ratio09 AS `13mois09`,
				y.salaire10 / y.ratio_total * y.ratio10 AS `13mois10`,
				y.salaire11 / y.ratio_total * y.ratio11 AS `13mois11`,
				y.salaire12 / y.ratio_total * y.ratio12 AS `13mois12`,

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
													YEAR(p.end_date) = %(fiscal_year)s
											) AS t  
											WHERE t.date_begin BETWEEN t.date_debut AND t.date_fin 
							) v
							GROUP BY v.employee) AS w) AS y 
				""", {"fiscal_year":self.fiscal_year}, as_dict=1
			)

			for i in liste:
				frappe.msgpint(str(i))
				
				

		

