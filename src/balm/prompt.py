'''
Created on Aug 8, 2023

@author: immanueltrummer
'''
class PromptGenerator():
    """ Generates prompts for language models. """
    
    def __init__(self, task, examples):
        """ Initializes prompt generator for specific task.
        
        Args:
            task: natural language description of task.
            examples: samples as list of input-output tuples.
        """
        self.task = task
        self.examples = examples
    
    def prompt(self, text):
        """ Generate prompt to process given text.
        
        Args:
            process task on this text.
        
        Returns:
            a prompt processing task on text, possibly with samples.
        """
        parts = [self.example(*example) for example in self.examples]
        parts += [self.example(text)]
        return '\n\n'.join(parts)
    
    def example(self, example_input, example_output=None):
        """ Generates text describing example.
        
        Args:
            example_input: input for example.
            example_output: output for example (optional).
        
        Returns:
            text describing the example.
        """
        prefix = example_input + '\n' + self.task
        if example_output is None:
            return prefix
        else:
            return prefix + '\n' + example_output