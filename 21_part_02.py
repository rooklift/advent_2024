# OK, basic idea:
#
# For each level, have an object storing:
# - The keys that are actually pressed e.g. 029A at top level.
# - The sequences that need to be pressed by the robot below.
#
# e.g. to move to push   0: <A
#                        2: ^A
#                        9: ^^>A
#                        A: vvvA
#
# Since each of those sequences below ends in A, the order of
# those sequences doesn't matter, so store a dict of:
#
# - sequence --> count of them
#
# e.g. {
#         "<A"   : 1,
#         "^A"   : 1,
#         "^^>A" : 1,
#         "vvvA" : 1,
# }
#
# There's some subtleties since one sequence can be better than another.
#
# But then it should be easy to cache what the best way to generate each
# of the possible sequences is.

