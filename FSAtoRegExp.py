'''
  TCS2021
  Assignment #3
  FSAtoRegExp

  @author Aliaksei Korshuk
  @version 1.0
  @since   2021-04-25
'''

class Translator(object):
    '''
    Class of FSA to RegExp Translator
    '''

    def __init__(self, fileNameIn, fileNameOut):
        '''
        Constructor with parament
        :param fileNameIn: File to read
        :param fileNameOut: File to write
        '''

        self.isErrorExist = False
        self.exception1 = ''
        self.exception2 = self.exception4 = self.exception0 = self.exception5 = False
        self.exception3 = ''
        self.fin = open(fileNameIn)
        self.fout = open(fileNameOut, 'w')

        # E0: Input file is malformed
        for i in range(5):
            try:
                command = self.fin.readline()
                start = command.find('[')
                end = command.find(']')
                commandNew = command[start + 1: end]
                if i == 0:
                    self.states = commandNew.split(",")
                    self.n = len(self.states)
                    if command.find("states=[") == -1 or end == -1:
                        self.exception0 = True
                        self.isErrorExist = True
                elif i == 1:
                    self.alpha = commandNew.split(",")
                    if command.find("alpha=[") == -1 or end == -1:
                        self.exception0 = True
                        self.isErrorExist = True
                elif i == 2:
                    self.initState = commandNew.split(",")
                    if command.find("initial=[") == -1 or end == -1:
                        self.exception0 = True
                        self.isErrorExist = True
                elif i == 3:
                    self.finState = commandNew.split(",")
                    if command.find("accepting=[") == -1 or end == -1:
                        self.exception0 = True
                        self.isErrorExist = True
                elif i == 4:
                    self.trans = commandNew.split(",")
                    if command.find("trans=[") == -1 or end == -1:
                        self.exception0 = True
                        self.isErrorExist = True
            except Exception:
                self.exception0 = True
                self.isErrorExist = True

    def depthFirstDearch(self, start, graph, visited_vertices, previous):
        '''
        Depth-first search algorithm
        :param start: Starting
        :param g: Array
        :param visited: Array of boolean values
        :param prev: Previous
        '''
        visited_vertices[start] = True
        for vertex in graph[start]:
            if not visited_vertices[vertex]:
                previous[vertex] = start
                self.depthFirstDearch(vertex, graph, visited_vertices, previous)

    def isError(self):
        '''
        Method that returns True if error exist
        :return: Boolean
        '''
        return self.isErrorExist

    def writeErrors(self):
        '''
        Method that writes error in file
        '''
        error_message = "Error:\n"
        if self.exception0:
            error_message += 'E0: Input file is malformed'
        elif self.exception1 != '':
            error_message += "E1: A state '"
            error_message += self.exception1
            error_message += "' is not in the set of states"
        elif self.exception2:
            error_message += 'E2: Some states are disjoint'
        elif self.exception3 != '':
            error_message += "E3: A transition '"
            error_message += self.exception3
            error_message += "' is not represented in the alphabet"
        elif self.exception4:
            error_message += 'E4: Initial state is not defined'
        elif self.exception5:
            error_message += 'E5: FSA is nondeterministic'
        self.fout.write(error_message)


    def check(self):
        '''
        Method that checks for errors
        :return:
        '''
        visited = []
        prev = []
        for i in range(self.n):
            visited.append(False)
            prev.append(None)

        graph = [[] for i in range(self.n)]


        # E4: Initial state is not defined
        if self.initState[0] == '':
            self.exception4 = True
            self.isErrorExist = True

        # E1: A state 's' is not in the set of states
        if self.initState[0] not in self.states:
            self.exception1 = self.initState[0]
            self.isErrorExist = True

        transitions = [[] for i in range(len(self.states))]

        # E3: A transition 'a' is not represented in the alphabet
        if not self.isErrorExist:
            for tran in self.trans:

                s1, a, s2 = tran.split('>')
                transitions[self.states.index(s1)].append(a)
                if s1 not in self.states:
                    self.exception1 = s1
                    self.isErrorExist = True
                    break
                fr = self.states.index(s1)
                if s2 not in self.states:
                    self.exception1 = s2
                    self.isErrorExist = True
                    break
                to = self.states.index(s2)
                if to != fr:
                    if to not in graph[fr]:
                        graph[fr].append(to)
                    if fr not in graph[to]:
                        graph[to].append(fr)
                if s1 not in self.states:
                    self.isErrorExist = True
                    self.exception1 = s1
                    break
                elif s2 not in self.states:
                    self.isErrorExist = True
                    self.exception1 = s2
                    break
                elif a not in self.alpha:
                    self.isErrorExist = True
                    self.exception3 = a
                    break

        # E5: FSA is nondeterministic
        for transition in transitions:
            for tran in self.trans:
                fr, a, to = tran.split('>')
                if a in transition and transition.count(a) == 1 or a not in transition:
                    continue
                else:
                    self.isErrorExist = True
                    self.exception5 = True

        # E2: Some states are disjoint
        self.depthFirstDearch(0, graph, visited, prev)
        if False in visited:
            self.isErrorExist = True
            self.exception2 = True


    def toRegExp(self):
        '''
        Translates FSA to RegExp
        '''
        final_states_index = []
        regex = self.private_get_init_regex(final_states_index)

        for k in range(len(self.states)):
            new_regex = [[0] * len(self.states) for i in range(len(self.states))]
            for i in range(len(self.states)):
                for j in range(len(self.states)):
                    new_regex[i][j] = "("
                    new_regex[i][j] += regex[i][k]
                    new_regex[i][j] += ")("
                    new_regex[i][j] += regex[k][k]
                    new_regex[i][j] += ")*("
                    new_regex[i][j] += regex[k][j]
                    new_regex[i][j] += ")|("
                    new_regex[i][j] += regex[i][j]
                    new_regex[i][j] += ")"
            regex = new_regex

        result_new_regex = ''

        for i in range(len(final_states_index)):
            result_new_regex += regex[0][final_states_index[i]] + "|"

        answer = ""
        if result_new_regex == '':
            answer += "{}"
        else:
            answer += str(result_new_regex[0:-1])
        self.fout.write(answer)

    def private_get_init_regex(self, fin_states_ind):
        '''
        Initial translation of FSA to RegExp
        :param fin_states_ind: States
        :return: Initial RegExp
        '''
        init_regex = [[''] * len(self.states) for i in range(len(self.states))]

        for i in range(len(self.states)):
            state = self.states[i]
            if state in self.finState:
                fin_states_ind.append(i)

        for i in range(len(self.states)):
            state = self.states[i]

            for j in range(len(self.states)):
                new_state = self.states[j]
                regex = ''
                for transition in self.trans:
                    trans_info = transition.split('>')
                    if trans_info[2] == new_state and trans_info[0] == state:
                        regex += trans_info[1] + "|"
                if state == new_state:
                    regex += "eps"
                if regex == '':
                    regex = "{}"
                if regex[-1] == "|":
                    regex = regex[0:-1]
                init_regex[i][j] = regex
        return init_regex


# Drive code
translator = Translator('input.txt', 'output.txt')
translator.check()

if translator.isError():
    translator.writeErrors()
else:
    translator.toRegExp()
