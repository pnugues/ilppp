import graph_utils

s1 = [{'id': '0', 'form': 'ROOT', 'head': '0', 'deprel': 'ROOT'},
      {'id': '1', 'form': 'the', 'head': '2', 'deprel': 'det'},
      {'id': '2', 'form': 'waiter', 'head': '3', 'deprel': 'sub'},
      {'id': '3', 'form': 'brought', 'head': '0', 'deprel': 'root'},
      {'id': '4', 'form': 'the', 'head': '5', 'deprel': 'det'},
      {'id': '5', 'form': 'meal', 'head': '3', 'deprel': 'obj'}]

s2 = [{'id': '0', 'form': 'ROOT', 'head': '0', 'deprel': 'ROOT'},
      {'id': '1', 'form': 'Um', 'head': '4', 'deprel': 'CP'},
      {'id': '2', 'form': 'ihn', 'head': '4', 'deprel': 'OA'},
      {'id': '3', 'form': 'dennoch', 'head': '4', 'deprel': 'MO'},
      {'id': '4', 'form': 'anzuschieben', 'head': '6', 'deprel': 'MO'},
      {'id': '5', 'form': ',', 'head': '6', 'deprel': 'PUNC'},
      {'id': '6', 'form': 'wollte', 'head': '0', 'deprel': 'ROOT'},
      {'id': '7', 'form': 'sich', 'head': '21', 'deprel': 'OA'},
      {'id': '8', 'form': 'die', 'head': '9', 'deprel': 'NK'},
      {'id': '9', 'form': 'Privatwirtschaft', 'head': '6', 'deprel': 'SB'},
      {'id': '10', 'form': 'erstmals', 'head': '6', 'deprel': 'MO'},
      {'id': '11', 'form': '``', 'head': '6', 'deprel': 'PUNC'},
      {'id': '12', 'form': 'in', 'head': '21', 'deprel': 'MO'},
      {'id': '13', 'form': 'erheblichem', 'head': '12', 'deprel': 'NK'},
      {'id': '14', 'form': 'Umfang', 'head': '12', 'deprel': 'NK'},
      {'id': '15', 'form': 'an', 'head': '21', 'deprel': 'OP'},
      {'id': '16', 'form': 'den', 'head': '15', 'deprel': '15'},
      {'id': '17', 'form': 'Risiken', 'head': '15', 'deprel': 'NK'},
      {'id': '18', 'form': '\'\'', 'head': '15', 'deprel': 'PUNC'},
      {'id': '19', 'form': 'der', 'head': '20', 'deprel': 'NK'},
      {'id': '20', 'form': 'Investition', 'head': '15', 'deprel': 'AG'},
      {'id': '21', 'form': 'beteiligen', 'head': '6', 'deprel': 'OC'},
      {'id': '22', 'form': '.', 'head': '6', 'deprel': 'PUNC'}]


def unit_tests():
    assert (graph_utils.nonprojective_links(s1)) == []
    assert (graph_utils.nonprojective_links(s2)) == [{'deprel': 'OA', 'id': '7', 'form': 'sich', 'head': '21'}]


unit_tests()
