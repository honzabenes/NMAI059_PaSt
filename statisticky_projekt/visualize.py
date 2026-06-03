import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def visualize_permutation_test(result, alpha=0.05):
	
	null_distribution_data = result.null_distribution
	observed_statistic = result.statistic

	# Vizuální styl s ohraničením (jako na obrázku)
	sns.set_theme(style="ticks")
	plt.figure(figsize=(7, 4.5))

	# 1. Vykreslení histogramu (stat='count' zajistí POČTY permutací na ose Y)
	# Barva je nastavena na podobnou šedomodrou s bílými okraji sloupečků
	sns.histplot(null_distribution_data, bins=60, color='#8CA1A9', stat='count', edgecolor='white')

	# 2. Výpočet kritické hodnoty pro JEDNOSTRANNÝ test (hladina významnosti 5 % zprava)
	critical_value = np.percentile(null_distribution_data, 100 - alpha * 100)

	# 3. Vystínování zamítací oblasti (od kritické hodnoty doprava)
	plt.axvspan(critical_value, plt.xlim()[1] * 1.2, color='#F3C999', alpha=0.8, 
			label='zamítací oblast (α = 0.01)')

	# 4. Svislé čáry (Kritická hodnota červeně, naše data tmavě zeleně)
	plt.axvline(critical_value, color='#D32828', linestyle='-', linewidth=2.5, 
			label=f'kritická hodnota = {critical_value:.2f}')
	plt.axvline(observed_statistic, color='#006B60', linestyle='-', linewidth=2.5, 
			label=f'T_obs = {observed_statistic:.2f} (our data)')

	# 5. Popisky a titulek
	plt.title('Rozdělení T pod $H_0$ (100,000 permutací) · jednostranně')
	plt.xlabel('Rozdíl průměrů')
	plt.ylabel('Počet permutací') 

	# Legenda vlevo nahoře s jemným okrajem
	plt.legend(loc='upper left', frameon=True)

	# Úprava zobrazení, aby graf neměl zbytečné prázdné okraje
	plt.xlim(min(null_distribution_data) - 0.2, max(observed_statistic, max(null_distribution_data)) + 0.2)
	plt.tight_layout()

	# Zobrazení
	plt.show()