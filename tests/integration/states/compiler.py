# -*- coding: utf-8 -*-

'''
tests for host state
'''

# Import python libs
import os

# Import Salt Testing libs
from salttesting.helpers import ensure_in_syspath
ensure_in_syspath('../../')

# Import salt libs
import integration
import salt.utils


class CompileTest(integration.ModuleCase):
    '''
    Validate the state compiler
    '''
    def test_multi_state(self):
        '''
        Test the error with multiple states of the same type
        '''
        ret = self.run_function('state.sls', mods='fuzz.multi_state')
        # Verify that the return is a list, aka, an error
        self.assertIsInstance(ret, list)

    def test_jinja_deep_error(self):
        '''
        Test when we have an error in a execution module
        called by jinja
        '''
        ret = self.run_function('state.sls', ['issue-10010'])
        self.assertTrue(
            ', in jinja_error' in ret[0].strip())
        self.assertTrue(
            ret[0].strip().endswith('Exception: hehehe'))

    def test_env_in_jinja_context(self):
        salt.utils.warn_until(
            'Boron',
            'We are only supporting \'env\' in the templating context until Boron comes out. '
            'Once this warning is show, please remove the test case',
            _dont_call_warnings=True
        )
        managed_file = os.path.join(integration.TMP, 'env-in-jinja-ctx.txt')
        template = [
            '{0}:'.format(managed_file),
            '  file.managed:',
            '    - contents: {{ saltenv }}'
        ]
        try:
            ret = self.run_function('state.template_str', ['\n'.join(template)], timeout=120)
            self.assertEqual('base', open(managed_file).read())
        finally:
            if os.path.isfile(managed_file):
                os.unlink(managed_file)

        template = [
            '{0}:'.format(managed_file),
            '  file.managed:',
            '    - contents: {{ env }}'
        ]
        try:
            ret = self.run_function('state.template_str', ['\n'.join(template)], timeout=120)
            self.assertEqual('base', open(managed_file).read())
        finally:
            if os.path.isfile(managed_file):
                os.unlink(managed_file)


if __name__ == '__main__':
    from integration import run_tests
    run_tests(CompileTest)
