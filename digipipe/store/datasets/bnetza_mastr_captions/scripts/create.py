import json
import re


def process() -> None:
    def replace_umlaut(s: str) -> str:
        replace_dict = {"ae": "ä", "oe": "ö", "ue": "ü", "Mastr": "MaStR"}
        for k, v in replace_dict.items():
            s = s.replace(k, v)
        return s

    # Build mapping dict
    naming_dict = dict()
    for mastr_config in snakemake.params.mastr_configs.values():
        for k, v in mastr_config.get("attributes", {}).items():
            if naming_dict.get(k, None) is None:
                naming_dict[v] = replace_umlaut(
                    re.sub("([a-z])([A-Z])", "\g<1> \g<2>", k)
                )

    naming_dict = {
        "datasets_caption_map": {
            _: "mastr" for _ in snakemake.params.mastr_configs.keys()
        },
        "captions": {"mastr": naming_dict},
    }

    # Dump as JSON while preserving umlaute
    with open(snakemake.output.outfile, "w", encoding="utf8") as f:
        json.dump(naming_dict, f, ensure_ascii=False, indent=4)


process()
