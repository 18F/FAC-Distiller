def apply_all_heuristics(data):
    """
    Apply all heuristics to the findings. CAP does not need any
    heuristics so far.
    """
    for heuristic in heuristics:
        data = heuristic(data)
    return data


def remove_toc(data):
    """
    Ignore the first two pages of a PDF, since these are likely to be
    a table of contents.
    """
    return list(filter(lambda d: int(d["page_number"]) > 2, data))


def handle_keyword_duplicates(data):
    """
    Sometimes keywords are combined together: "Condition, Context,
    Effect: ..." In this case, we remove duplicates and preserve the
    first keyword match.
    """
    def maybe_remove_duplicates(item):
        values = item.values()
        unique_values = set(values)
        if len(values) == len(unique_values):
            return item
        new_item = dict()
        for key, value in item.items():
            if value in unique_values:
                new_item[key] = value
                unique_values.remove(value)
        return new_item
    return [maybe_remove_duplicates(item) for item in data]


def strip_if_first_match(data):
    """
    If we have a keyword and we start with that keyword in the text,
    remove the match.
    """
    def maybe_strip_match(item):
        for key, value in item.items():
            value_str = str(value).lower()
            key_str = key.lower()
            if not value_str.startswith(key_str):
                yield (key, value)
                continue
            index = value_str.find(key_str) + len(key_str)
            new_value = value[index:]
            # optionally remove : and trailing space
            if new_value and new_value[0] == ':':
                new_value = new_value[1:]
            while new_value and new_value[0] == ' ':
                new_value = new_value[1:]
            yield (key, new_value)
    return [dict(maybe_strip_match(item)) for item in data]


heuristics = [
    remove_toc,
    handle_keyword_duplicates,
    strip_if_first_match,
]


if __name__ == '__main__':
    sample = [
        {'page_number': 37, 'Criteria': 'GREATER PORTLAND COUNCIL OF GOVERNMENTS', 'Condition': 'Condition: For the fiscal year ended June 30, 2017, the Greater Portland Council of Governments did not record federal expenditures of $83,644 in the proper period, and improperly excluded this amount from the respective financial statements and Schedule of Expenditures of Federal Awards SEFA.', 'Context': 'Context: As part of our compliance testing, we selected a sample of forty 40 transactions consisting of non- payroll expenditures for all projects under CFDA #20.205.', 'Effect': 'Effect: The effect of this finding was an understatement of federal expenditures for the fiscal year ended June 30, 2017 and an overstatement of the same for the fiscal year ended June 30, 2018.', 'effect': 'Effect: The effect of this finding was an understatement of federal expenditures for the fiscal year ended June 30, 2017 and an overstatement of the same for the fiscal year ended June 30, 2018.', 'Cause': 'Cause: Timing of the receipt invoices and management oversight.', 'Recommendation': 'Recommendation: We recommend that the Greater Portland Council of Governments review its current policies and procedures regarding the processing of expenditures, including those for federal award programs, to ensure proper presentation of its financial statements and Schedule of Expenditures of Federal Awards in the future.'},
        {'page_number': 41, 'Criteria': 'SIGNIFICANT DEFICIENCY', 'Condition': 'Condition, Context, Effect, Cause, Recommendation: As noted in finding #2018‐001 above, for the fiscal year ended June 30, 2017, the Greater Portland Council of Governments improperly excluded federal expenditures in the amount of $83,644 from the 2017 financial statements and the related Schedule of Expenditures of Federal Awards SEFA.', 'Context': 'Condition, Context, Effect, Cause, Recommendation: As noted in finding #2018‐001 above, for the fiscal year ended June 30, 2017, the Greater Portland Council of Governments improperly excluded federal expenditures in the amount of $83,644 from the 2017 financial statements and the related Schedule of Expenditures of Federal Awards SEFA.', 'Effect': 'Condition, Context, Effect, Cause, Recommendation: As noted in finding #2018‐001 above, for the fiscal year ended June 30, 2017, the Greater Portland Council of Governments improperly excluded federal expenditures in the amount of $83,644 from the 2017 financial statements and the related Schedule of Expenditures of Federal Awards SEFA.', 'Cause': 'Condition, Context, Effect, Cause, Recommendation: As noted in finding #2018‐001 above, for the fiscal year ended June 30, 2017, the Greater Portland Council of Governments improperly excluded federal expenditures in the amount of $83,644 from the 2017 financial statements and the related Schedule of Expenditures of Federal Awards SEFA.', 'Recommendation': 'Condition, Context, Effect, Cause, Recommendation: As noted in finding #2018‐001 above, for the fiscal year ended June 30, 2017, the Greater Portland Council of Governments improperly excluded federal expenditures in the amount of $83,644 from the 2017 financial statements and the related Schedule of Expenditures of Federal Awards SEFA.', 'effect': 'It had no effect on our planned or required testing of the federal programs.', 'response': 'Questioned Costs: None Views of responsible officials and planned corrective action: See management’s response and corrective action in Section IV of this Schedule of Findings and Questioned Costs.'}
    ]
    result = apply_all_heuristics(sample)
    print(result)
