import copy
import json
from pathlib import Path
import unittest
from rlworkbench.contracts import validate_modules


def module(mid, role='representation', deployment=True):
    return {'id':mid,'role':role,'deployment':deployment,
            'inputs':[{'name':'observation','source':'external:observation','available_at':'decision_time','privilege':'agent'}],
            'outputs':['value'],'persistent_state':[], 'update_clock':'environment_arrival',
            'objective':'Predict a declared target','measure':'Held-out causal prediction error and downstream return',
            'downstream_consumers':[],'costs':['forward FLOPs'], 'evidence_status':'proposed'}


def wire(parent,child,lag='decision_time',privilege='agent'):
    parent['downstream_consumers'].append(child['id'])
    child['inputs'].append({'name':parent['id']+'_value','source':parent['id']+'.value','available_at':lag,'privilege':privilege})


class ContractTests(unittest.TestCase):
    def test_optional_and_good_single_module(self):
        self.assertEqual(validate_modules({}),[])
        self.assertEqual(validate_modules({'modules':[module('encode')]}),[])

    def test_missing_metadata_is_not_silently_defaulted(self):
        m=module('encode'); del m['deployment']
        self.assertTrue(validate_modules({'modules':[m]}))

    def test_unique_ids_input_names_and_references(self):
        a,b=module('a'),module('b');wire(a,b)
        self.assertEqual(validate_modules({'modules':[a,b]}),[])
        for mutation in ('duplicate','bad_output','unknown','missing_backref'):
            ms=copy.deepcopy([a,b])
            if mutation=='duplicate':ms.append(copy.deepcopy(ms[0]))
            if mutation=='bad_output':ms[1]['inputs'][-1]['source']='a.nonexistent'
            if mutation=='unknown':ms[0]['downstream_consumers'].append('nonexistent')
            if mutation=='missing_backref':ms[0]['downstream_consumers']=[]
            with self.subTest(mutation=mutation):self.assertTrue(validate_modules({'modules':ms}))

    def test_diagnostic_branch_is_allowed_if_isolated(self):
        d=module('oracle',role='diagnostic',deployment=False)
        d['inputs'][0].update(source='external:hidden_state',privilege='diagnostic')
        self.assertEqual(validate_modules({'modules':[d]}),[])

    def test_diagnostic_taint_cannot_be_laundered_by_middle_module(self):
        d=module('oracle','diagnostic',False);d['inputs'][0]['privilege']='diagnostic'
        m=module('model','world_model',False);a=module('policy','actor',True)
        wire(d,m);wire(m,a)
        errors=validate_modules({'modules':[d,m,a]})
        self.assertTrue(any('policy: diagnostic privilege' in e for e in errors))

    def test_delaying_privileged_information_does_not_make_it_legal(self):
        d=module('oracle','diagnostic',False);d['inputs'][0]['privilege']='diagnostic'
        a=module('policy','actor',True);wire(d,a,'previous_lifetime')
        self.assertTrue(any('diagnostic privilege' in e for e in validate_modules({'modules':[d,a]})))

    def test_delayed_recurrent_cycle_is_allowed(self):
        a,b=module('memory'),module('policy','actor')
        wire(a,b);wire(b,a,'previous_step')
        self.assertEqual(validate_modules({'modules':[a,b]}),[])

    def test_algebraic_same_cycle_is_rejected(self):
        a,b=module('memory'),module('policy','actor')
        wire(a,b);wire(b,a)
        self.assertTrue(any('same-cycle' in e for e in validate_modules({'modules':[a,b]})))

    def test_actor_cannot_hide_deployment_role(self):
        a=module('actor','actor',False)
        self.assertTrue(validate_modules({'modules':[a]}))

    def test_no_source_inference_from_future_label_names(self):
        m=module('m');m['inputs'][0]['source']='a.value'
        self.assertTrue(validate_modules({'modules':[m]}))

    def test_template_is_structurally_valid_but_only_proposed(self):
        path=Path(__file__).resolve().parents[1]/'templates/module-contract.json'
        template=json.loads(path.read_text())
        self.assertEqual(validate_modules(template),[])
        self.assertTrue(all(m['evidence_status']=='proposed' for m in template['modules']))

    def test_malformed_enum_returns_errors_not_type_error(self):
        for field in ('available_at','privilege'):
            m=module('m');m['inputs'][0][field]=[]
            self.assertTrue(validate_modules({'modules':[m]}))
        m=module('m');m['evidence_status']={}
        self.assertTrue(validate_modules({'modules':[m]}))


if __name__=='__main__':unittest.main()
