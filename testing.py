import re
string = """# Chinese Youth Slang: "Rùn"

Chinese youths have adopted the slang term "rùn," meaning to flee, as a way to express their desire to escape various pressures, including parental expectations and the challenges of urban life. Over time, it has evolved to signify emigrating from China altogether, with an increasing number of individuals seeking legal migration to Europe or America. Some even take bold routes, like traversing the dangerous Darien Gap to reach Mexico and the United States, contributing to the migrant surge at the southern U.S. border.

# Diverse Escape Routes

The preferred destinations for those using the term "rùn" vary, including Singapore, Japan, and Thailand. The latter, in particular, has become a haven for a diverse group of individuals, ranging from remote workers and spiritual seekers to crypto enthusiasts and even drug users. The author notes that meeting such individuals in Thailand has left him feeling somewhat optimistic about China's future, suggesting that the creative minds escaping might contribute positively to the country they'll eventually inherit.

## Changing Demographics and Challenges

China, aspiring to be a global superpower, faces challenges as its demographic landscape undergoes contraction. The author highlights the irony of a youthful talent pool seeking escape, with aspiring artists and entrepreneurs opting for unconventional destinations like the highlands of Thailand over major Chinese cities. This trend raises concerns about the overall health and vibrancy of China's economic and cultural future.

### Geopolitical Dynamics

Geopolitically, the author suggests that while a significant portion (50%) of China's economy may be dysfunctional, the remaining 5% that performs exceptionally well poses a considerable threat to American interests. This threat encompasses booming automobile exports and an expanding defense industrial base. The complexity of navigating this dynamic further adds to the challenges faced by the United States on the global stage.

# America's Peculiar Situation

The notes conclude by highlighting the peculiar situation of the United States in 2024. Despite being perceived as an empire in decline, the country is facing challenges on multiple fronts from revisionist powers. The metaphor of juggling a worldwide array of commitments made during a time of unchallenged power emphasizes the complexities and uncertainties the U.S. grapples with on the global stage."""

string2 = "# jflsljdfkls \n# sfs"

insights = re.split('#', string)
insights = ['####' + insight for insight in insights if insight != '']
for insight in insights:
  print("new insight:")
  print(insight)
print("len: ", len(insights))