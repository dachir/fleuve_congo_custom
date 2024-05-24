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
		self.details.clear()

		if not self.details:
			liste = frappe.db.sql(
				"""
				
				SELECT t.annee, t.mois, t.date_begin, t.date_end, t.date_join, t.date_debut, t.date_fin, t.date_quit, t.employee,
					(t.start_period_day / t.period_day * t.rate) + t.years_div_5 AS new_rate, t.period_day, t.rate, t.salaire, t.start_period_day, t.years_difference, t.years_div_5, t.categorie, %(parent)s AS parent, 'details' AS parentfield, 'Provision' AS parenttype
				FROM (
					SELECT 
						e.name as employee, 
						YEAR(p.end_date) AS Annee, 
						MONTH(p.end_date) AS Mois,
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
						YEAR(p.end_date) = %(end_date)s
				) AS t  
				WHERE t.date_begin BETWEEN t.date_debut AND t.date_fin 
				""", {"parent":self.name,"end_date":self.fiscal_year}
			)

			for i in liste:
				frappe.throw(str(i))
				self.append(
						"details",
						{
							"annee": i.annee,
							"mois": i.mois,
							"periode_date_begin": i.date_begin,
							"periode_date_end": i.date_end,
							"date_join": i.date_join,
							"date_begin": i.date_begin,
							"periode_date_end": i.date_end,
							"date_begin": i.date_debut,
							"date_end": i.date_fin,
							"date_quit": i.date_quit,
							"employee": i.employee,
							"new_rate": i.new_rate,
							"period_days": i.period_day,
							"rate": i.rate,
							"salaire": i.salaire,
							"start_period_days": i.start_period_day,
							"years_difference": i.years_difference,
							"year_div_5": i.years_div_5,
							"categorie": i.categorie,
						},
					)
				


	def before_save(self):
		self.add_details()

	def after_insert(self):
		self.add_details()
		

