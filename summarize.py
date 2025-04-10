# Use a pipeline as a high-level helper
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

article = "Leaders of more than 30 countries from Latin America and the Caribbean have promised to take measures to boost trade within the region to minimise the impact of President Trump's tariffs. At the leaders' summit in Honduras, Brazilian president Luiz Inacio Lula da Silva said that arbitrary tariffs would destabilise the international economy and cause inflation. Mexico's president Claudia Sheinbaum said they \"require unity and solidarity among their governments and peoples and to strengthen greater regional integration\" Both leaders said, however, they would try to negotiate with the Trump administration before considering retaliatory tariffs. Analysts say the tariffs may increase Chinese economic presence in Latin America and the Caribbean. China was invited to attend the summit as a special guest."

response = summarizer(article, max_length=130, min_length=30, do_sample=False)