# VYGENEROVÁNO GEMINI
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def visualize_permutation_test(result, alpha=0.05, alternative='two-sided', 
                               title='Výsledek permutačního testu', 
                               xlabel='Rozdíl průměrů', 
                               ylabel='Počet permutací'):
    """
    Univerzální funkce pro vizualizaci permutačního testu.
    
    Parametry:
    - result: výstup z funkce scipy.stats.permutation_test
    - alpha: hladina významnosti (default: 0.05)
    - alternative: 'two-sided', 'greater', nebo 'less'
    - title: Nadpis grafu
    - xlabel: Popisek osy X
    - ylabel: Popisek osy Y
    """
    null_distribution_data = result.null_distribution
    observed_statistic = result.statistic

    sns.set_theme(style="ticks")
    plt.figure(figsize=(7, 4.5))

    # 1. Vykreslení histogramu
    sns.histplot(null_distribution_data, bins=60, color='#8CA1A9', stat='count', edgecolor='white')
    x_min, x_max = plt.xlim()

    # 2. Výpočet kritických hodnot a stínování podle typu testu
    if alternative == 'two-sided':
        percentile_lower = (alpha / 2) * 100
        percentile_upper = 100 - (alpha / 2) * 100
        cv_lower = np.percentile(null_distribution_data, percentile_lower)
        cv_upper = np.percentile(null_distribution_data, percentile_upper)

        plt.axvspan(x_min - abs(x_min), cv_lower, color='#F3C999', alpha=0.8, label=f'zamítací oblast (α = {alpha})')
        plt.axvspan(cv_upper, x_max + abs(x_max), color='#F3C999', alpha=0.8)
        
        plt.axvline(cv_lower, color='#D32828', linestyle='-', linewidth=2.5, label=f'kritické hodnoty = {cv_lower:.2f}, {cv_upper:.2f}')
        plt.axvline(cv_upper, color='#D32828', linestyle='-', linewidth=2.5)
        
        plot_min = min(min(null_distribution_data), observed_statistic, cv_lower) - 0.2
        plot_max = max(max(null_distribution_data), observed_statistic, cv_upper) + 0.2

    elif alternative == 'greater':
        cv = np.percentile(null_distribution_data, 100 - alpha * 100)
        
        plt.axvspan(cv, x_max + abs(x_max), color='#F3C999', alpha=0.8, label=f'zamítací oblast (α = {alpha})')
        plt.axvline(cv, color='#D32828', linestyle='-', linewidth=2.5, label=f'kritická hodnota = {cv:.2f}')
        
        plot_min = min(min(null_distribution_data), observed_statistic) - 0.2
        plot_max = max(max(null_distribution_data), observed_statistic, cv) + 0.2

    elif alternative == 'less':
        cv = np.percentile(null_distribution_data, alpha * 100)
        
        plt.axvspan(x_min - abs(x_min), cv, color='#F3C999', alpha=0.8, label=f'zamítací oblast (α = {alpha})')
        plt.axvline(cv, color='#D32828', linestyle='-', linewidth=2.5, label=f'kritická hodnota = {cv:.2f}')
        
        plot_min = min(min(null_distribution_data), observed_statistic, cv) - 0.2
        plot_max = max(max(null_distribution_data), observed_statistic) + 0.2

    else:
        raise ValueError("Parametr 'alternative' musí být 'two-sided', 'greater', nebo 'less'.")

    # 3. Vykreslení naší skutečné statistiky
    plt.axvline(observed_statistic, color='#006B60', linestyle='-', linewidth=2.5, 
                label=f'T_obs = {observed_statistic:.2f} (naše data)')

    # 4. Popisky a titulek
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='upper left', frameon=True)

    # Úprava zobrazení osy X, aby vše bylo vidět
    plt.xlim(plot_min, plot_max)
    plt.tight_layout()
    plt.show()


def visualize_regression(x, y, title='Vztah mezi proměnnými', 
                         xlabel='Osa X', ylabel='Osa Y'):
    """
    Vykreslí bodový graf s proloženou regresní přímkou pro původní data.
    """
    sns.set_theme(style="ticks")
    plt.figure(figsize=(7, 4.5))

    # 1. Vykreslení samotných bodů (hráčů)
    # Použijeme stejnou modrošedou barvu jako pro histogram, s lehkou průhledností
    sns.scatterplot(x=x, y=y, color='#8CA1A9', alpha=0.6, edgecolor='none')

    # 2. Výpočet regresní přímky (y = k*x + q) pomocí NumPy
    slope, intercept = np.polyfit(x, y, 1)

    # 3. Vytvoření souřadnic pro vykreslení přímky (od nejmenšího x po největší)
    x_line = np.array([min(x), max(x)])
    y_line = slope * x_line + intercept

    # 4. Vykreslení regresní přímky (tmavě zelenou barvou, jako T_obs)
    plt.plot(x_line, y_line, color='#006B60', linewidth=2.5, 
             label=f'Regresní přímka (sklon = {slope:.4f})')

    # 5. Popisky a titulek
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.legend(loc='upper left', frameon=True)
    plt.tight_layout()
    plt.show()