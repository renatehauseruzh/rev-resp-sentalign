# Representing sentence alignments in gold standard?

## Review Response Sentence Alignment

- json format 
- need to isolate pickle/store tokenizater for reproducibility
- sentence IDs are enumerated beginning at 1
- alignment "4": ["2", "3"] indicates review sentence 4 aligns with responses sentences 2 and 3.

```
{
	{
		"docid": 3165203,
		"review": [
			"Best Rehoboth wedding retreat.",
			"---SEP---",
			"We so enjoyed our stay at the Bell for.",
			"We did not have time to take advantage of the spa or pools but definitely, enjoyed the breakfast, shady outdoor areas, and convenience to the beach.",
			"We look forward to returning."
		],
		"response": [
			"Thank you for the response!",
			"We encourage you to come back for a return visit so you can enjoy all those things you missed out on this time.",
			"The Bellmoor is not the same without enjoying our spa or pools.",
			"We hope to see you soon."
		],
		"sent_alignment": {
			"4": ["2", "3"]
		}
	}

	{
		"docid": 3207998,
		"review": [
			"right next to the airport, friendly staff ---SEP--- Check in was smooth.",
			"The front desk was very friendly.",
			"The room was clean.",
			"The breakfast was standard Hampton Inn.",
			"The breakfast area was busy, but things filled up quickly.",
			"There were three hot items (eggs, sausage, bacon or home fries).",
			"The hotel was really close to the airport, so you can definitely hear the airplanes flying over.",
			"It was a little noisy for me.",
			"And there were no restaurants in walking distance.",
			"There is a gas station and 7-11 right next door."
		],
		"response":
			[
				"I am pleased that you were satisfied with the service and accommodations here.",
				"The team and I look forward to again hosting your stay during your visit in the Charlotte area.",
			],
		"sent_alignment": {
			"2": ["1"],
			"3": ["1"]
		}
	}	
}

```



## Inspiration for representing alignment...

Newsela corpus (ATS)
- TSV format
- do not include sentence IDs, but rather raw tokenized text

```
DOC1    V1      V4      American women will soon be free to fight on the front lines of battle and they will go with the public 's support .    American women will soon be able to fight in wars .
```

Zurich's PaCoCo (multilingual parallel corpora)
- TSV format
- stand-off alignments with alignment unit IDs for doc-, sent- and word-level



