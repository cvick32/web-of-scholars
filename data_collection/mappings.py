string_to_wikidata_key = {
    "doctoral_advisor": "P184",
    "doctoral_student": "P185",
    "field": "P101",
    "image": "P18",
}

"""
This is a map from names of attributes to the list of attributes
that are needed to call on a list of attributes to get the desired
field. Let's try an example:

Scholar 101 = {
    "claims": ...
    "aliases": {
        "en": [{"value": "Cole Vick"}, "]
        "es": ...
        ...
    }
    ...
}

So to get the correct name out of this structure we need to navigate 
to the `aliases` object, then select english as the language, then 
select the first position of the array, then select the value of that
object. So, it would be exactly the array described below to find the 
name, if we iterate over the attributes, as we do in the function
`get_value_from_attributes` below.
"""
name_to_attribute = {
    "advisors": ["claims", string_to_wikidata_key["doctoral_advisor"]],
    "field": [
        "claims",
        string_to_wikidata_key["field"],
        0,
        "mainsnak",
        "datavalue",
        "value",
        "id",
    ],
    "image": [
        "claims",
        string_to_wikidata_key["image"],
        0,
        "mainsnak",
        "datavalue",
        "value",
    ],
    "name": ["aliases", "en", 0, "value"],
    "other_name": ["aliases", "en", "value"],
    "title_name": ["labels", "en", "value"],
    "scholar_qid": ["mainsnak", "datavalue", "value", "id"],
    "students": ["claims", string_to_wikidata_key["doctoral_student"]],
    "wiki_link": ["sitelinks", "enwiki", "url"],
}
