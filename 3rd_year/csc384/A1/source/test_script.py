
# import student's functions
from solution import *
from test_problems import PROBLEMS

#Select what to test
test_manhattan = False
test_fval_function = False
test_alternate = False
test_anytime_weighted_astar = False
test_anytime_gbfs = False

if test_manhattan:
    ##############################################################
    # TEST MANHATTAN DISTANCE
    print('Testing Manhattan Distance')

    #Correct Manhattan distances for the initial states of the provided problem set
    correct_man_dist = [6,4,4,11,5,5,6,7,9,5]

    solved = 0; unsolved = []

    for i in range(0, 10):
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]

        man_dist = heur_manhattan_distance(s0)
        print('calculated man_dist:', str(man_dist))

        print(s0.state_string()) #To see state

        if man_dist == correct_man_dist[i]:
            solved += 1
        else:
            unsolved.append(i)    

    print("*************************************")  
    print("In the problem set provided, you calculated the correct Manhattan distance for {} states out of 10.".format(solved))  
    print("States that were incorrect: {}".format(unsolved))      
    print("*************************************\n") 
    ##############################################################

if test_fval_function:

  test_state = SnowmanState("START", 6, None, None, None, None, None, None, None)

  correct_fvals = [6, 11, 16]

  ##############################################################
  # TEST fval_function
  print("*************************************") 
  print('Testing fval_function')

  solved = 0
  weights = [0., .5, 1.]
  for i in range(len(weights)):

    test_node = sNode(test_state, hval=10, fval_function=fval_function)

    fval = fval_function(test_node, weights[i])
    print ('Test', str(i), 'calculated fval:', str(fval), 'correct:', str(correct_fvals[i]))
    
    if fval == correct_fvals[i]:
      solved +=1  

  print("\n*************************************")  
  print("Your fval_function calculated the correct fval for {} out of {} tests.".format(solved, len(correct_fvals)))  
  print("*************************************\n") 
  ##############################################################

if test_alternate:

  ##############################################################
  # TEST ALTERNATE HEURISTIC
  print('Testing alternate heuristic with best_first search')

  solved = 0; unsolved = []; benchmark = 15; timebound = 8 #time limit
  
  for i in range(0, len(PROBLEMS)): 

    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    print(s0.state_string())
    se = SearchEngine('best_first', 'full')
    se.init_search(s0, goal_fn=snowman_goal_state, heur_fn=heur_simple)
    final = se.search(timebound)

    if final:
      final.print_path()  
      solved += 1
    else:
      unsolved.append(i)

  print("\n*************************************")
  print("Of {} initial problems, {} were solved in less than {} seconds by this solver.".format(len(PROBLEMS), solved, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("The benchmark implementation solved {} out of {} practice problems given {} seconds.".format(benchmark,len(PROBLEMS),timebound))
  print("*************************************\n")
  ##############################################################
  

if test_anytime_gbfs:

  len_benchmark = [37, 15, 19, 36, 35, 60, 18, 22, 34, 28]

  ##############################################################
  # TEST ANYTIME GBFS
  print('Testing Anytime GBFS')

  solved = 0; unsolved = []; benchmark = 0; timebound = 8 #8 second time limit 
  for i in range(0, 10):
    print("*************************************")  
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    weight = 10
    final = anytime_gbfs(s0, heur_fn=heur_alternate, timebound=timebound)

    if final:
      final.print_path()   
      if final.gval <= len_benchmark[i] or len_benchmark[i] == -99:
        benchmark += 1
      solved += 1 
    else:
      unsolved.append(i)  

  print("\n*************************************")  
  print("Of 10 initial problems, {} were solved in less than {} seconds by this solver.".format(solved, timebound))  
  print("Of the {} problems that were solved, the cost of {} matched or outperformed the benchmark.".format(solved, benchmark))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))  
  print("The benchmark implementation solved 10 out of the 10 practice problems given 8 seconds.")  
  print("*************************************\n") 

if test_anytime_weighted_astar:

  len_benchmark = [37, 15, 19, 36, 35, 60, 18, 22, 34, 28, 32, 43, 37, 88, -99, 40, -99, -99, -99, -99]

  ##############################################################
  # TEST ANYTIME WEIGHTED A STAR
  print('Testing Anytime Weighted A Star')

  solved = 0; unsolved = []; benchmark = 0; timebound = 8 #8 second time limit 
  for i in range(0, 20):
    print("*************************************")  
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    weight = 10
    final = anytime_weighted_astar(s0, heur_fn=heur_alternate, weight=weight, timebound=timebound)

    if final:
      final.print_path()   
      if final.gval <= len_benchmark[i] or len_benchmark[i] == -99:
        benchmark += 1
      solved += 1 
    else:
      unsolved.append(i)  

  print("\n*************************************")  
  print("Of 20 initial problems, {} were solved in less than {} seconds by this solver.".format(solved, timebound))  
  print("Of the {} problems that were solved, the cost of {} matched or outperformed the benchmark.".format(solved, benchmark))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))  
  print("The benchmark implementation solved 15 out of the 20 practice problems given 8 seconds.")  
  print("*************************************\n") 
  ##############################################################

