# Copyright (c) 2024, Kossivi Amouzou and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PreparationProvisionDecompte(Document):
	def before_save(self):
		if self.employee :
			emp = frappe.get_doc('Employee',self.employee)
			self.salaire = emp.salaire_de_base

			date_actuelle_end = frappe.utils.getdate(self.fin_contrat)
			date_entree_end = frappe.utils.getdate(self.date_embauche)
			# Calculate the difference in years
			years = date_actuelle_end.year - date_entree_end.year

			jour_entree = date_entree_end.day
			mois_entree = date_entree_end.month
			jour_actuelle = date_actuelle_end.day
			mois_actuelle = date_actuelle_end.month


			date_entree_end = frappe.utils.getdate(self.date_embauche)  # mamadate d'entrée (par exemple)
			date_actuelle_end = frappe.utils.getdate(self.fin_contrat)  # madate actuelle (par exemple)

			# Différence en années
			years = date_actuelle_end.year - date_entree_end.year
			if date_actuelle_end.month < date_entree_end.month or (date_actuelle_end.month == date_entree_end.month and date_actuelle_end.day < date_entree_end.day):
				years = years

			# Différence en mois
			months = date_actuelle_end.month - date_entree_end.month
			if date_actuelle_end.day < date_entree_end.day :
				months = months - 1
			if months < 0 :
				months = months + 12
				years = years - 1

			# Comparer seulement les jours du mois
			if date_actuelle_end.day >= date_entree_end.day:
				days = date_actuelle_end.day - date_entree_end.day
			else:
				previous_month = (date_actuelle_end.month - 1) if date_actuelle_end.month > 1 else 12
				previous_year = date_actuelle_end.year if date_actuelle_end.month > 1 else date_actuelle_end.year - 1
				days_in_previous_month = (frappe.utils.getdate(f"{previous_year}-{previous_month + 1}-01") - frappe.utils.getdate(f"{previous_year}-{previous_month}-01")).days
				days = (date_actuelle_end.day + int(days_in_previous_month)) - date_entree_end.day

			# Affichage des résultats
			self.ancienneté_details = str(years) + " ans, " +  str(months) + " mois, " + str(days) + "jours"

			#self.anciennete = years
			self.anciennete = years

			if days == 0 :
				self.conge_compensatoire = months * 1.5
			else :
				self.conge_compensatoire = (months + 1) * 1.5
				
			if days == 0 :
				self.gratification13è_mois = ((mois_actuelle - 1) * 26) / 12
			else :
				self.gratification13è_mois = ((mois_actuelle) * 26) / 12

			preavis_days = 0


			if (emp.categories == "MANŒUVRE" or emp.categories == "SEMI-QUALIFIE" or emp.categories == "HAUTEMENT QUALIFIE"):
				
				preavis_days = 7 * years
				emp.preavis_days = ( preavis_days + 14 ) / 2
					
			elif (emp.categories == "AGENT DE MAITRISE"):
				preavis_days = 9 * years
				emp.preavis_days = ( preavis_days + 26 ) / 2
			elif (emp.categories == "CADRE DE COLLABORATION" or emp.categories == "CADRE DE DIRECTION"):
				preavis_days = 16 * years
				emp.preavis_days =  (preavis_days + 78) / 2
			else :
				self.anciennete = years
				
			self.conge__sur_préavis = (self.preavis_days * 26) / (26 * 12)

