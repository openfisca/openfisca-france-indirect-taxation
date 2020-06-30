import pandas as pd

results = pd.DataFrame(columns = ['revenu_reforme_officielle_2019_in_2017', ])

results['revenu_reforme_officielle_2019_in_2017'] = [
    177.8786111189104,
    124.0368540474721,
    102.96654540613808,
    109.22812348840685,
    117.74523480020078,
    127.02319511375342,
    125.59710506015722,
    136.58329030191015,
    147.88585060158798,
	173.68750897282365,
    ]

results['cheques_energie'] = [
    165.1208649984687,
    82.43152192369013,
    26.972320532973487,
    12.969241415962086,
    10.085249732963657,
    5.157410570397746,
    2.0150545274444127,
    2.3846946782823446,
    0.8543932861507411,
    0.1014845968530853,
    ]

results['tarifs_sociaux_electricite'] = [
    65.5388,
    21.46009870218798,
    7.539849422277608,
    4.629126210795642,
    3.0531693830956637,
    2.031803631214231,
    0.5270967096364093,
    0.8739232632701135,
    0.29072541885025116,
    0.0,
    ]

results['tarifs_sociaux_gaz'] = [
    30.355182501663556,
    11.20197537685839,
    2.8531176169425887,
    2.0614055491184624,
    1.0639069792215494,
    0.7981500886043917,
    0.27272000846580957,
    0.38152450917427727,
    0.11296018243967688,
    0.0,
    ]

results.index += 1
