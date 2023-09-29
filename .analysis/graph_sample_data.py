import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

# empty the graph directory if it exists, otherwise create it
if os.path.exists('../graphs'):
    files = glob.glob('../graphs/*.pdf')
    for f in files:
        os.remove(f)
else:
    os.makedirs('../graphs')

# load the data
act_df = pd.read_csv(
    "../data/V1-during-hackathon/gpt_generated_data/gpt-turbo-temp-1-annotations-0-99-20230816021421-persona-activist.csv")
act_df["persona"] = "Activist-Egalitarian"
prt_df = pd.read_csv(
    "../data/V1-during-hackathon/gpt_generated_data/gpt-turbo-temp-1-annotations-0-99-20230816015112-persona-prudent.csv")
prt_df["persona"] = "Prudent-Traditionalist"

df = pd.concat([act_df, prt_df], ignore_index=True)

df = df.applymap(lambda s: s.lower() if type(s) == str else s)
df['gender'] = df['gender'].apply(lambda x: x.title() if type(x) == str else x)
df['occupation'] = df['occupation'].apply(lambda x: x.title() if type(x) == str else x)
df['name'] = df['name'].apply(lambda x: x.title() if type(x) == str else x)

unique_personas = [p for p in df['persona'].unique()]

plot_types = ['Gender Distribution', 'Top 5 Occupations', 'Age Distribution', 'Top 5 Names']

for i, persona in enumerate(unique_personas):
    persona_df = df[df['persona'] == persona]

    for j, plot_type in enumerate(plot_types):
        fig, ax = plt.subplots(figsize=(8, 6))

        if plot_type == 'Gender Distribution':
            sns.countplot(data=persona_df, y='gender', ax=ax, palette='pastel')
            ax.set_ylabel('')
            ax.set_title(f'Gender Distribution\nbased on a sample of a hundred GPT generated {persona} personas',
                         fontsize=16)
        elif plot_type == 'Top 5 Occupations':
            occupation_counts = persona_df['occupation'].value_counts().head(5)
            sns.barplot(y=occupation_counts.index, x=occupation_counts.values, ax=ax, palette='coolwarm')
            ax.set_ylabel('')
            ax.set_title(f'Occupation Distribution\nbased on a sample of a hundred GPT generated {persona} personas',
                         fontsize=16)
        elif plot_type == 'Age Distribution':
            sns.histplot(data=persona_df, x='age', bins=30, ax=ax, palette='viridis')
            ax.set_title(f'Age Distribution\nbased on a sample of a hundred GPT generated {persona} personas',
                         fontsize=16, fontstyle='normal')
            ax.set_ylabel('Count', fontsize=14)
            ax.set_xticks(
                range(min(persona_df['age']), max(persona_df['age']) + 1, 5))
            ax.tick_params(axis='x', labelsize=12)
        elif plot_type == 'Top 5 Names':
            name_counts = persona_df['name'].value_counts().head(5)
            sns.barplot(y=name_counts.index, x=name_counts.values, ax=ax, palette='muted')
            ax.set_ylabel('')
            ax.set_title(f'Top 5 Names\nbased on a sample of a hundred GPT generated {persona} personas', fontsize=16)

        ax.set_xlabel('Count', fontsize=14)
        ax.tick_params(labelsize=12)

        plt.tight_layout()

        plt.savefig(f'../graphs/{persona.replace(" ", "_")}_{plot_type.replace(" ", "_").lower()}.pdf', bbox_inches='tight',
                    dpi=300)

        plt.close(fig)
