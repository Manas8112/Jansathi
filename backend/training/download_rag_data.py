import json
import urllib.request
import os

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "../data/datasets/sample_laws.json")

def download_real_laws():
    print("Downloading massive real dataset for RAG...")
    
    # We will fetch a large dataset of legal QA and Acts from an open GitHub repo
    # This repo contains thousands of QA pairs on Indian Law
    url = "https://raw.githubusercontent.com/OpenNyAI/Opennyai/master/datasets/legal_qa/dev.json"
    
    try:
        req = urllib.request.urlopen(url)
        data = json.loads(req.read())
    except Exception as e:
        print(f"Failed to fetch dataset: {e}")
        return

    laws = []
    
    for item in data:
        # Format it into our schema
        laws.append({
            "title": item.get("context_title", "Indian Legal Code"),
            "type": "law_section",
            "source": "OpenNyAI Dataset",
            "text": item.get("context", "")
        })
        
        # Stop after 500 massive context chunks to keep ChromaDB fast but impressive
        if len(laws) >= 500:
            break

    # Also add our core acts for the specific hackathon use cases
    core_acts = [
        {
            "title": "Right to Information Act, 2005 - Section 6",
            "type": "bare_act",
            "source": "rti.gov.in",
            "text": "Section 6(1): A person, who desires to obtain any information under this Act, shall make a request in writing or through electronic means in English or Hindi or in the official language of the area in which the application is being made, accompanying such fee as may be prescribed, to the Central Public Information Officer or State Public Information Officer, as the case may be, of the concerned public authority; (b) the Central Assistant Public Information Officer or State Assistant Public Information Officer, as the case may be, specifying the particulars of the information sought by him or her."
        },
        {
            "title": "Right to Information Act, 2005 - Section 7",
            "type": "bare_act",
            "source": "rti.gov.in",
            "text": "Section 7(1): Subject to the proviso to sub-section (2) of section 5 or the proviso to sub-section (3) of section 6, the Central Public Information Officer or State Public Information Officer, as the case may be, on receipt of a request under section 6 shall, as expeditiously as possible, and in any case within thirty days of the receipt of the request, either provide the information on payment of such fee as may be prescribed or reject the request for any of the reasons specified in sections 8 and 9."
        },
        {
            "title": "Consumer Protection Act, 2019 - Section 35",
            "type": "bare_act",
            "source": "consumeraffairs.nic.in",
            "text": "Section 35: Manner in which complaint shall be made. (1) A complaint, in relation to any goods sold or delivered or agreed to be sold or delivered or any service provided or agreed to be provided, may be filed with a District Commission by— (a) the consumer to whom such goods are sold or delivered or agreed to be sold or delivered or such service provided or agreed to be provided; (b) any recognised consumer association whether the consumer to whom the goods sold or delivered or agreed to be sold or delivered or service provided or agreed to be provided is a member of such association or not; (c) one or more consumers, where there are numerous consumers having the same interest, with the permission of the District Commission, on behalf of, or for the benefit of, all consumers so interested; or (d) the Central Authority, the Central Government or the State Government, as the case may be, either in its individual capacity or as a representative of interests of the consumers in general."
        },
        {
            "title": "Real Estate (Regulation and Development) Act, 2016 - Section 18",
            "type": "bare_act",
            "source": "mohua.gov.in",
            "text": "Section 18: Return of amount and compensation. (1) If the promoter fails to complete or is unable to give possession of an apartment, plot or building,— (a) in accordance with the terms of the agreement for sale or, as the case may be, duly completed by the date specified therein; or (b) due to discontinuance of his business as a developer on account of suspension or revocation of the registration under this Act or for any other reason, he shall be liable on demand to the allottees, in case the allottee wishes to withdraw from the project, without prejudice to any other remedy available, to return the amount received by him in respect of that apartment, plot, building, as the case may be, with interest at such rate as may be prescribed in this behalf including compensation in the manner as provided under this Act."
        }
    ]
    
    laws.extend(core_acts)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(laws, f, indent=2)
        
    print(f"Successfully saved {len(laws)} massive legal documents to sample_laws.json!")
    print("Now you just need to run: python -m knowledge.ingest to put them into the Vector DB!")

if __name__ == "__main__":
    download_real_laws()
