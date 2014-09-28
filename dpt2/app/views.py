from django.core.urlresolvers import reverse
from models import *
from registration.backends.simple.views import RegistrationView
from shortcuts import render, redirect, render_to_response
import tempfile
import subprocess
import os
import datetime
import random
#import matrix
#import dpt2Matrix
import math
import operator

global Big_Matrix


def main(request):
    if not request.user.is_authenticated():
        return redirect(reverse('registration_register'))
    # if 'version' in request.session:
    #     version = request.session['version']
    #     print "Taking Version from Session"
    # else:
    #     print "Taking Version from DB"
    try:
        version = Version.objects.filter()[0]
    except IndexError:
        version = Version(date=datetime.datetime.now())
        version.save()
    a = [[], [], [], []]
    if version:
        products = Product.objects.filter(version=version, selectable=True)
        for i in range(products.count() / 4):
            a[0].append(products[4 * i])
            a[1].append(products[4 * i + 1])
            a[2].append(products[4 * i + 2])
            a[3].append(products[4 * i + 3])
    products = a
    # global Big_Matrix
    # Big_Matrix = eval(BigMatrix.objects.get(version = version).matrix)
    # Big_Matrix = dpt2Matrix.Big_Matrix
    # changing to custom page to test- change from main.html to dinestart.html
    return render(request, 'main.html', {'products': products, 'version': version})


# return render_to_response('dinestart.html')

##created dinestart to render 'dinebase.html and dinepreferences.html'
#def dinestart(request):
#	return render_to_response('dinepreferences.html')

def versions(request):
    versions = Version.objects.all()
    return render(request, 'versions.html', {'versions': versions})


def my_foodie(request):  #reinier
    return redirect('/login')


#	if not request.user.id:
#		return redirect('/login')
#	return render(request, 'my_foodie.html', {'versions': versions})

def random_meal(request):  #reinier
    # if 'version' in request.session:
    #     version = request.session['version']
    # else:
    try:
        version = Version.objects.order_by('-id')[0]
    except IndexError:
        return redirect('/')
    products = Product.objects.filter(version=version)
    output = len(products)
    random_num = random.randint(1, len(products) - 1)
    meal = products[random_num]
    return render(request, 'random_meal.html', {'versions': versions, 'output': output, 'meal': meal})


def VIP(request):  #Chums
    return render(request, 'VIP.html', {'versions': versions})


def about(request):  #reinier
    return render(request, 'about.html', {'versions': versions})


def intro1(request):
    return render(request, 'intro1.html', {'versions': versions})


def intro2(request):
    return render(request, 'intro2.html', {'versions': versions})


def intro3(request):
    return render(request, 'intro3.html', {'versions': versions})


def intro4(request):
    return render(request, 'intro4.html', {'versions': versions})


def intro5(request):
    return render(request, 'intro5.html', {'versions': versions})


def intro6(request):
    return render(request, 'intro6.html', {'versions': versions})


def intro7(request):
    return render(request, 'intro7.html', {'versions': versions})


def intro8(request):
    return render(request, 'intro8.html', {'versions': versions})


def intro9(request):
    return render(request, 'intro9.html', {'versions': versions})


def set_version(request, version_id):
    try:
        version = Version.objects.get(id=version_id)
    except Version.DoesNotExist:
        return redirect('/')
    request.session['version'] = version
    return redirect('/')


def calc_pos(x, y):  #WORKS This is correct for the number of stimuli specified
    #requires: a valid meal pair
    #returns the position in the x-axis of the pair (x,y)
    numStimuli = 25
    if ((y <= x) or (y < 0) or (x < 0) or (x > (numStimuli - 1)) or (y > numStimuli)):
        return "Invalid: calc pos out of bounds"
    pos = 0
    for i in range(1, x):
        pos = pos + numStimuli - i
    pos = pos + (y - x)
    return pos - 1


def get_pair(pos):  #WORKS  for the number of stimuli specified
    #requires: the position of the pair in the x axis of the matrix
    #returns: a tuple of the (x,y) pair
    numStimuli = 25
    numPairs = math.factorial(numStimuli) / (
        2 * math.factorial(numStimuli - 2))  #calculates how many possible pairs can be formed by that number of stimuli
    if ((pos >= numPairs) or (pos < 0)):
        return "INVALID: get_pair out of bounds"
    n = numStimuli - 1
    x = 1
    y = 1
    while ((pos - n) >= 0):
        x += 1
        y += 1
        pos = pos - n
        n -= 1
    y = y + pos + 1
    return (x, y)


def eliminate_redundant(pair1, pair2):
    #requires: two pairs with one index in common
    #returns: three unique ints corresponding to the three meals that should be selected
    for x in pair2:
        if x not in pair1:
            return pair1[0], pair1[1], x


def get_score(percent, sum_across_product, numFncs, ABS_NUM_ROW):
    #requires: the percent of pos distances
    #requires: the sum of the abs val of the distances
    #returns: the score corresponding to the inputted values
    return ((percent * (1 - percent)) / .25) * (float(sum_across_product) / ((ABS_NUM_ROW - 1) * numFncs))


def get_score_list(BM, rows_eliminated_set):
    #requires: the matrix with x-values corresponding to pairs and y to Utility functions
    #requires: a list of the rows_eliminated
    #requires: the num of Utility Fncs remaining
    #returns: a list of the scores for each pair
    ######the perecnt of positive ditances for each pair in a list and sum of the abs val of the distances
    NUM_PAIRS = len(BM)  #-1
    numFncs = len(BM[0]) - len(rows_eliminated_set) - 1
    num_pos = [0] * NUM_PAIRS
    sum_across_product_order = [0] * NUM_PAIRS
    score = [0] * NUM_PAIRS
    for i in range(NUM_PAIRS):  #+1): #added +1
        for j in range(len(BM[0])):
            if j not in rows_eliminated_set:
                if BM[i][j] >= 0:
                    num_pos[i] += 1
                sum_across_product_order[i] += abs(BM[i][j])

        percent = num_pos[i] / float(numFncs)
        score[i] += get_score(percent, sum_across_product_order[i], numFncs, len(BM[0]))
    return score


def get_third_meal(max_pair, scores, NUM_PAIRS):
    #gets the third meal given a pair of meals
    #requires: the max pair and the list of scores
    #returns: the third meal
    #print 'Pair: '+str(max_pair)+'\nSCORES: '+str(scores)+'\nNUM_PAIRS: '+str(NUM_PAIRS)
    numStimuli = 25
    third_product_scores = [0] * (NUM_PAIRS + 1)  # #added +1
    for x in range(1, numStimuli + 1):
        if (x > max_pair[0]):
            a = calc_pos(max_pair[0], x)
            third_product_scores[a] = scores[a]
        if (x < max_pair[0]):
            a = calc_pos(x, max_pair[0])
            third_product_scores[a] = scores[a]
        if (x > max_pair[1]):
            b = calc_pos(max_pair[1], x)
            third_product_scores[b] = scores[b]
        if (x < max_pair[1]):
            b = calc_pos(x, max_pair[1])
            third_product_scores[b] = scores[b]
        third_product_scores[calc_pos(max_pair[0], max_pair[1])] = -float("inf")  #0
    max_third_index = third_product_scores.index(max(third_product_scores))
    max_third_pair = get_pair(max_third_index)
    (meal1, meal2, meal3) = eliminate_redundant(max_pair, max_third_pair)
    return meal3


def get_meals(BM, rows_eliminated):
    #BM=BM.matrix
    rows_eliminated_set = set(rows_eliminated)
    NUM_PAIRS = len(BM) - 1
    ABS_NUM_ROW = len(BM[0]) - 1
    numFncs = ABS_NUM_ROW - len(rows_eliminated) - 1  #calculate the number of functions remaining
    scores = get_score_list(BM, rows_eliminated_set)  #gets the list of scores corresponding to each pair
    max_index = scores.index(max(scores))  #gets the index of the max score
    max_pair = get_pair(max_index)  #first two meals to show
    meal1 = max_pair[0]
    meal2 = max_pair[1]
    meal3 = get_third_meal(max_pair, scores, NUM_PAIRS)
    return (meal1, meal2, meal3)


def start(request):
    global Big_Matrix
    if not request.user.is_authenticated():
        return redirect(reverse('registration_register'))
    # if 'version' in request.session:
    #     version = request.session['version']
    # else:
    try:
        version = Version.objects.order_by('-id')[0]
    except IndexError:
        version = Version(date=datetime.datetime.now())
        version.save()
    rnd = Round(version=version, user=request.user, date=datetime.datetime.now())
    rnd.save()
    products = Product.objects.filter(selectable=True)
    (a, b, c) = random.sample(products, 3)
    poll = Poll(round=rnd, product_a=a, product_b=b, product_c=c, date=datetime.datetime.now())

    #	(a,b,c)=get_meals(Big_Matrix, [])
    #	poll = Poll(round=rnd, product_a=Product.objects.get(stimuliNum = a, version = version), product_b=Product.objects.get(stimuliNum = b, version = version), product_c=Product.objects.get(stimuliNum = c, version = version), date=datetime.datetime.now())

    poll.save()
    #	(a,b,c)=get_meals(BigMatrix.objects.get(version = version).matrix, [])#bad_functions)
    #	poll = Poll(round=rnd, product_a=Product.objects.get(oid = a, version = version), product_b=Product.objects.get(oid = b, version = version), product_c=Product.objects.get(oid = c, version = version), date=datetime.datetime.now())
    #	poll.save()
    return redirect('/preferences')


def preferences(request):
    try:
        rnd = Round.objects.filter(user=request.user).order_by('-id')[0]
    except IndexError:
        return redirect('/')
    polls = Poll.objects.select_related().filter(round=rnd).order_by('-id')
    if not polls:
        return redirect('/start')
    poll = polls[0]
    polls_count = polls.count()
    print "polls count", polls_count
    return render(request, 'preferences.html', {'poll': poll, 'numPolls': polls_count})


def choose(request):
    # if 'version' in request.session:
    #     version = request.session['version']
    # else:
    try:
        version = Version.objects.order_by('-id')[0]
    except IndexError:
        return redirect('/')
    rnd = Round.objects.filter(user=request.user).order_by('-id')[0]
    use_random = 1
    #print >>sys.stderr, 'at Line 260'
    polls = [p for p in Poll.objects.select_related().filter(round=rnd).order_by('-id')]
    if not polls:
        return redirect('/start')
    poll = polls[0]  # look at last poll
    poll.choice = Product.objects.get(id=request.POST['id'])  # id of product just picked
    poll.save()  # save the choices they just made

    polls.reverse()  # polls in order from oldest to newest
    choices = []  # fill with every choice that the person has made thus far
                  # (REINER-you could eliminate winners bc no more info can be gleaned
    ordered_choices = []
    for poll in polls:
        for p in [poll.product_a, poll.product_b, poll.product_c]:
            if not p in choices:
                choices.append(p)
        not_selected = [p for p in [poll.product_a, poll.product_b, poll.product_c] if p != poll.choice]
        ordered_choices.append([poll.choice, not_selected[0]])  # (one chose, one not chose)
        ordered_choices.append([poll.choice, not_selected[1]])

    property_ids = [x.id for x in Property.objects.filter(version=version)]
    function_ids = [f.id for f in Function.objects.filter(version=version)]
    function_properties = FunctionProperty.objects.select_related().filter(function__id__in=function_ids).values_list(
        'function_id', 'property_id', 'value')
    f_properties = {}
    for fid in function_ids:
        f_properties[fid] = {}  # coefficients
    for p in function_properties:
        f_properties[p[0]][p[1]] = p[2]

    product_properties = ProductProperty.objects.select_related().filter(product__in=choices).values_list('product_id',
                                                                                                          'property_id',
                                                                                                          'value')

    p_coefficients = {}
    for p in choices:
        p_coefficients[p.id] = {}
    for c in product_properties:
        p_coefficients[c[0]][c[1]] = c[2]

    last_bad_functions = []
    bad_functions = []  # go thu all UF and see if one of those pairs is violated
    ### bad functions always gets created??
    for listing in ordered_choices:
        print "listing", listing
        if len(ordered_choices) > 2 and listing == ordered_choices[-2]:
            last_bad_functions = [x for x in bad_functions]  # if every UF has been violated then revert to last state
        for function_id in function_ids:
            score_listing = []
            for product in listing:
                score = 0
                for property_id in property_ids:
                    try:
                        score += f_properties[function_id][property_id] * p_coefficients[product.id][property_id]
                    except (KeyError, AttributeError):
                        print "KeyError"
                score_listing.append(score)
            if score_listing[0] < score_listing[1]:
                if not function_id in bad_functions:
                    bad_functions.append(function_id)
                ## Work on before
                ## Transitiv

    #print >>sys.stderr, 'at Line 316'
    finals = []
    print function_ids, bad_functions, last_bad_functions
    if len(function_ids) - len(bad_functions) == 1:
        finals = [f for f in function_ids if f not in bad_functions]
        print finals
    if len(function_ids) == len(bad_functions):
        finals = [f for f in function_ids if f not in last_bad_functions]
        print finals
    if len(bad_functions) == len(last_bad_functions):
        finals = [f for f in function_ids if f not in last_bad_functions]
        print finals
    if finals:
        for final in finals:
            result = Result(round=rnd, function_id=final)
            result.save()
        return redirect('/results')
    else:
        print "No finals"

    if use_random == 1:
        used = []
        for poll in polls:
            used.append(poll.product_a)
            used.append(poll.product_b)
            used.append(poll.product_c)
        products = [p for p in Product.objects.filter(version=version, selectable=True) if p not in used]
        if len(products) < 3:
            products = Product.objects.filter(version=version, selectable=True)
        (a, b, c) = random.sample(products, 3)
        poll = Poll(round=rnd, product_a=a, product_b=b, product_c=c, date=datetime.datetime.now())
        poll.save()
    else:
        global Big_Matrix
        (a, b, c) = get_meals(Big_Matrix, bad_functions)
        #print 'a is' + str(a)
        #print 'b is' + str(b)
        #print 'c is' + str(c)

        poll = Poll(round=rnd, product_a=Product.objects.get(stimuliNum=a, version=version),
                    product_b=Product.objects.get(stimuliNum=b, version=version),
                    product_c=Product.objects.get(stimuliNum=c, version=version), date=datetime.datetime.now())
        poll.save()

    #print >>sys.stderr, 'Before getMeals'


    return redirect('/preferences')


def results(request, page=None):
    # if 'version' in request.session:
    #     version = request.session['version']
    # else:
    try:
        version = Version.objects.order_by('-id')[0]
    except IndexError:
        return redirect('/')
    rnd = Round.objects.filter(user=request.user).order_by('-id')[0]
    results = Result.objects.filter(round=rnd)
    property_ids = [x.id for x in Property.objects.filter(version=version)]
    function_ids = [r.function_id for r in results]
    function_properties = FunctionProperty.objects.select_related().filter(function__id__in=function_ids).values_list(
        'function_id', 'property_id', 'value')
    properties = {}
    for p in property_ids:
        properties[p] = 0

    for p in function_properties:
        try:
            properties[p[1]] += p[2]
        except KeyError:
            pass

    for i in properties.keys():
        properties[i] /= len(function_ids) or 1


    products = Product.objects.filter(version=version)
    product_properties = ProductProperty.objects.select_related().filter(product__in=products).values_list('product_id',
                                                                                                           'property_id',
                                                                                                           'value')
    p_coefficients = {}
    #print 'len products is ' + str(len(products))
    for p in products:
        p_coefficients[p.id] = {}
    #print p
    for c in product_properties:
        p_coefficients[c[0]][c[1]] = c[2]
    #print c

    allProps = Property.objects.filter(version=version)

    myStr = 'allProps is ('
    for pr in allProps:
        myStr = myStr + 'id = ' + str(pr.id) + ' & name is: ' + pr.name + ', '

    #print myStr + ')'
    products = products.values()
    for product in products:
        score = 0
        for property_id in property_ids:
            try:
                score += properties[property_id] * p_coefficients[product['id']][property_id]
            except KeyError:
                print "KeyError"
        product['score'] = score
    products = sorted(products, key=lambda k: k['score'])
    products.reverse()

    FoodVery = 0.0
    FoodSome = 0.0
    AroundVery = 0.0
    AroundSome = 0.0
    MoneyVery = 0.0
    MoneySome = 0.0
    SafetyVery = 0.0
    SafetySome = 0.0
    StressVery = 0.0
    StressSome = 0.0
    myStr = 'FinalUF is ('
    for property_id in property_ids:
        myProp = Property.objects.filter(version=version, id=property_id)
        if "Food" in myProp[0].name and "somewhat" in myProp[0].name:
            FoodSome = properties[property_id]
        if "Food" in myProp[0].name and "very" in myProp[0].name:
            FoodVery = properties[property_id]
        if "Around" in myProp[0].name and "somewhat" in myProp[0].name:
            AroundSome = properties[property_id]
        if "Around" in myProp[0].name and "very" in myProp[0].name:
            AroundVery = properties[property_id]
        if "Money" in myProp[0].name and "somewhat" in myProp[0].name:
            MoneySome = properties[property_id]
        if "Money" in myProp[0].name and "very" in myProp[0].name:
            MoneyVery = properties[property_id]
        if "Safety" in myProp[0].name and "somewhat" in myProp[0].name:
            SafetySome = properties[property_id]
        if "Safety" in myProp[0].name and "very" in myProp[0].name:
            SafetyVery = properties[property_id]
        if "Stress" in myProp[0].name and "somewhat" in myProp[0].name:
            StressSome = properties[property_id]
        if "Stress" in myProp[0].name and "very" in myProp[0].name:
            StressVery = properties[property_id]
        myStr = myStr + str(property_id) + ' = ' + str(properties[property_id]) + ', '

    print myStr + ')'

    print 'Money very: ' + str(MoneyVery)
    print 'Stress some: ' + str(StressVery)

    totalRange = 0.0
    rangeFood = max(0, FoodVery, FoodSome) - min(0, FoodVery, FoodSome)
    totalRange += rangeFood
    rangeAround = max(0, AroundVery, AroundSome) - min(0, AroundVery, AroundSome)
    totalRange += rangeAround
    rangeMoney = max(0, MoneyVery, MoneySome) - min(0, MoneyVery, MoneySome)
    totalRange += rangeMoney
    rangeSafety = max(0, SafetyVery, SafetySome) - min(0, SafetyVery, SafetySome)
    totalRange += rangeSafety
    rangeStress = max(0, StressVery, StressSome) - min(0, StressVery, StressSome)
    totalRange += rangeStress

    importances = {}
    if (FoodVery <= 0 and FoodSome <= 0) or rangeFood < (.01 * totalRange):
        importances['Food '] = 0.0
    else:
        importances['Food'] = rangeFood / totalRange
    if (AroundVery <= 0 and AroundSome <= 0) or rangeAround < (.01 * totalRange):
        importances['Getting Around '] = 0.0
    else:
        importances['Getting Around'] = rangeAround / totalRange
    if (MoneyVery <= 0 and MoneySome <= 0) or rangeMoney < (.01 * totalRange):
        importances['Money '] = 0.0
    else:
        importances['Money'] = rangeMoney / totalRange
    if (SafetyVery <= 0 and SafetySome <= 0) or rangeSafety < (.01 * totalRange):
        importances['Safety'] = 0.0
    else:
        importances['Safety'] = rangeSafety / totalRange
    if (StressVery <= 0 and StressSome <= 0) or rangeStress < (.01 * totalRange):
        importances['Stress '] = 0.0
    else:
        importances['Stress'] = rangeStress / totalRange

    importances = sorted(importances.iteritems(), key=operator.itemgetter(1), reverse=True)

    bestProduct = Product.objects.filter(version=version, oid=products[0]['oid'])

    #print bestProduct.values()

    bestProdValues = ProductProperty.objects.filter(product=bestProduct)

    #for i in range(0,4):
    #	print 'product[' + str(i) + '] is ' + products[i]['name'] + ' score is ' + str(products[i]['score'])
    #	myStr = 'product[' + str(i) + '] value is: ('
    #	for property_id in property_ids:
    #		myStr = myStr + str(p_coefficients[products[i]['id']][property_id]) + ', '
    #	print myStr + ')'

    pages = []
    for i in range(len(products) / 8):
        pages.append(products[8 * i:8 * i + 8])

    products = products[:8]

    polls = Poll.objects.filter(round=rnd)
    GraphData.objects.get_or_create(
        user=request.user,
        data=json.dumps(importances),
    )
    return render(request, 'results.html',
                  {'results': results, 'products': products, 'polls': polls, 'pages': pages, 'properties': properties,
                   'property_ids': property_ids, 'topTopic': importances[0][0], 'importances': importances})


class CustomRegistrationView(RegistrationView):
    """
    A registration backend which implements the simplest possible
    workflow: a user supplies a username, email address and password
    (the bare minimum for a useful account), and is immediately signed
    up and logged in).

    """


    def get_success_url(self, request, user):
        return reverse('start')
