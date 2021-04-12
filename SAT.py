#!/usr/bin/env python
# coding: utf-8

# # Introduction

# *Author: Hector R. Santos Marte*
# 
# The SAT is a multiple-choice exam with three sections: reading, writing and math, each of which is worth a maximum of 800 points. The purpose of the SAT is to measure high school student's readiness for college and provide colleges with one common data point that can be used to compare all applicants. A High average SAT scores is usually indicative of a good school.
# 
# There are currently debates about whether the SAT is a fair and non-discriminatory test. **My objective in this project is to analyze the relationship between different variables and the SAT results.**
#  
# New York City has a significant immigrant population and is very diverse, so comparing demographic factors such as: race, income, and gender with the SAT scores in NYC could provide me with some useful information. New York City has published high schools average SAT score data, along with additional complementary data sets, of which I will be using the following:
# 
# 1. SAT scores by school - SAT scores for each high school in New York City
# 2. School attendance - Attendance information for each school in New York City
# 3. Class size - Information on class size for each school
# 4. AP test results - Advanced Placement (AP) exam results for each high school (passing an optional AP exam in a particular subject can earn a student college credit in that subject)
# 5. Graduation outcomes - The percentage of students who graduated, and other outcome information
# 6. Demographics - Demographic information for each school
# 7. School survey - Surveys of parents, teachers, and students at each school
# 

# In[1]:


import pandas as pd
import numpy
import re
import os
import pprint
import seaborn as sns
import warnings

os.chdir('C:\\Users\\hecto\\Desktop\\Python Working Directory\\SAT Data')
os.getcwd()


# In[2]:


data_files = [
    "ap_2010.csv",
    "class_size.csv",
    "demographics.csv",
    "graduation.csv",
    "hs_directory.csv",
    "sat_results.csv"
]

data = {}

for f in data_files:
    d = pd.read_csv("C:\\Users\\hecto\\Desktop\\Python Working Directory\\SAT Data\\{0}".format(f))
    data[f.replace(".csv", "")] = d


# In[3]:


for key in data:
    print(key)
    print('\n')
    pprint.pprint( data[key].columns)
    print('\n')


# ## Obeservations:
# 
# - **DBN** :Every school in the system can be identified by its 6-digit code (DBN). The first two numbers represent the school district. The third character of the school code signifies the borough in which the school is located (M = Manhattan, X = Bronx, R = Staten Island, K = Brooklyn and Q = Queens). The final three digits are unique within borough
# 
# ## *Class-size*:
# 
# - The data set doesn't have a DBN column -which is our key column for merging all the data. DBN is the sum of CSD and School Code, but the CSD has a 0 to the left of each number in the other data sets. This need to be corrected before creating the DBN column
# 
# - The grade column should only inclue high school students, which is “09-12"
# 
# - In the Program Type Column, I would only leave 'GEN ED' , because the other program types are focused on kids with special needs. Here's the explanation for each:
# 
#      **General Education (GE)** :General education classes are those classes not coded as special education, integrated co-teaching, gifted and talented, or accelerated. 
# 
#      **Gifted and Talented (G&T)** : G&T classes are identified as classes in grades K-5 where students have been placed through the DOE’s G&T screening process.
# 
#      **Integrated Co-Teaching (Formerly Collaborative Team Teaching or CTT)** : Integrated Co-Teaching (ICT) ensures that students with disabilities are educated alongside age-appropriate peers in a general education setting.
# 
#      **Self-contained Special Education(SPEC ED)**: Self-contained special education classrooms, are those with IEP defining specific student/teacher/paraprofessional ratios. The ratio of students to teachers and paraprofessionals (Setting) is denoted as 12:1, 12:1:1, etc.
#      
#     **Accelerated Courses** : Middle school accelerated courses are high school credit-bearing courses offered to middle school students.
#     
# - The data set has multiple rows for the same DBN, it should be condensed
# 
# 
# ## *Demographics*:
# 
# - The data set has multiple rows for the same DBN,it should be condensed
# - The school years should be 2011 2012
# 
# ## *Graduation*:
# 
# - The data set has multiple rows for the same DBN, it should be condensed 
# - Reduce de data set to only total cohort in the Demographic column

# # Read in the surveys

# In[4]:


all_survey = pd.read_csv("survey_all.txt", delimiter="\t", encoding='windows-1252')
d75_survey = pd.read_csv("survey_d75.txt", delimiter="\t", encoding='windows-1252')
survey = pd.concat([all_survey, d75_survey], axis=0)

# Creating a DBN columns by copying the dbn column
survey["DBN"] = survey["dbn"]


# There are many unnecessary columns, so I will erase them. Here is a list of the ones staying:
#     
# - dbn: School identification code (district borough number)
# - rr_s: Student Response Rate
# - rr_t: Teacher Response Rate
# - rr_p: Parent Response Rate
# - N_s: Number of student respondents
# - N_t: Number of teacher respondents
# - N_p: Number of parent respondents
# - nr_s: Number of eligible students
# - nr_t: Number of eligible teachers
# - nr_p: Number of eligible parents
# - saf_p_11: Safety and Respect score based on parent responses
# - com_p_11: Communication score based on parent responses
# - eng_p_11: Engagement score based on parent responses
# - aca_p_11: Academic expectations score based on parent responses
# - saf_t_11: Safety and Respect score based on teacher responses
# - com_t_11: Communication score based on teacher responses
# - eng_t_11: Engagement score based on teacher responses
# - aca_t_11: Academic expectations score based on teacher responses
# - saf_s_11: Safety and Respect score based on student responses
# - com_s_11: Communication score based on student responses
# - eng_s_11: Engagement score based on student responses
# - aca_s_11: Academic expectations score based on student responses
# - saf_tot_11: Safety and Respect total score
# - com_tot_11: Communication total score
# - eng_tot_11: Engagement total score
# - aca_tot_11: Academic Expectations total score

# In[5]:


survey_fields = [
    "DBN", 
    "rr_s", 
    "rr_t", 
    "rr_p", 
    "N_s", 
    "N_t", 
    "N_p", 
    "saf_p_11", 
    "com_p_11", 
    "eng_p_11", 
    "aca_p_11", 
    "saf_t_11", 
    "com_t_11", 
    "eng_t_11", 
    "aca_t_11", 
    "saf_s_11", 
    "com_s_11", 
    "eng_s_11", 
    "aca_s_11", 
    "saf_tot_11", 
    "com_tot_11", 
    "eng_tot_11", 
    "aca_tot_11",
]
survey = survey.loc[:,survey_fields]
data["survey"] = survey


# # Add DBN columns

# In[6]:


# Renaming the dbn column to DBN in the hs_directory
data["hs_directory"].rename(columns={'dbn':'DBN'},inplace=True)
data["hs_directory"].columns


# In[7]:


# Creating a function for padding the CSD in the class_size data set
def pad_csd(num):
    string_representation = str(num)
    if len(string_representation) > 1:
        return string_representation
    else:
        return "0" + string_representation
    
# Creating a Padded  CSD column and creating the DBN column using the padded csd column in the class_size data set    
data["class_size"]["padded_csd"] = data["class_size"]["CSD"].apply(pad_csd)
data["class_size"]["DBN"] = data["class_size"]["padded_csd"] + data["class_size"]["SCHOOL CODE"]
data["class_size"]["DBN"].head(3)


# # Convert columns to numeric

# In[8]:


#converting some columns in the sat_results data set to numeric
cols = ['SAT Math Avg. Score', 'SAT Critical Reading Avg. Score', 'SAT Writing Avg. Score']
for c in cols:
    data["sat_results"][c] = pd.to_numeric(data["sat_results"][c], errors="coerce")
    
#Creating an sat_score column in the sat_reults data set
data['sat_results']['sat_score'] = data['sat_result`s'][cols[0]] + data['sat_results'][cols[1]] + data['sat_results'][cols[2]]


# In[9]:


#Extracting the latitud and longitude from the locaton_1 column in the hs_directory data set

pd.set_option('max_colwidth', 1000)
data["hs_directory"]["Location 1"].head(3)


# **The latitude and longitude are inside the parentheses.**

# In[10]:


#Creating two functions : one for the extracting the  latitude and  for the longitude. 

def find_lat(loc):
    coords = re.findall("\(.+, .+\)", loc)
    lat = coords[0].split(",")[0].replace("(", "")
    return lat

def find_lon(loc):
    coords = re.findall("\(.+, .+\)", loc)
    lon = coords[0].split(",")[1].replace(")", "").strip()
    return lon
#One column for each is created in the hs_directory data set 
data["hs_directory"]["lat"] = data["hs_directory"]["Location 1"].apply(find_lat)
data["hs_directory"]["lon"] = data["hs_directory"]["Location 1"].apply(find_lon)
     
data["hs_directory"]["lat"] = pd.to_numeric(data["hs_directory"]["lat"], errors="coerce")
data["hs_directory"]["lon"] = pd.to_numeric(data["hs_directory"]["lon"], errors="coerce")

data["hs_directory"][['Location 1','lat','lon']].head(3)


# In[11]:


## Convert AP scores to numeric
cols = ['AP Test Takers ', 'Total Exams Taken', 'Number of Exams with scores 3 4 or 5']

for col in cols:
    data["ap_2010"][col] = pd.to_numeric(data["ap_2010"][col], errors="coerce")


# # Condense datasets

# In[12]:


#Filtering the data set class_size to only include data from high school students and general education programs
class_size = data["class_size"]
class_size = class_size[class_size["GRADE "] == "09-12"]
class_size = class_size[class_size["PROGRAM TYPE"] == "GEN ED"]
class_size.head(3)


# In[13]:


#Grouping the DBNs that are repeated in several rows into a single one, where the values of the other numeric columns will be average
class_size = class_size.groupby("DBN").agg(numpy.mean)
class_size.reset_index(inplace=True)
data["class_size"] = class_size
data["class_size"].head(3)


# In[14]:


#Filtering the demographics data set to only include the 2011-2012 school year
data["demographics"] = data["demographics"][data["demographics"]["schoolyear"] == 20112012]


# In[15]:


#Filtering the graduation data set to include the entire group, instead of some subgroup and, the last year, which in this case is 2006
data["graduation"] = data["graduation"][data["graduation"]["Cohort"] == "2006"]
data["graduation"] = data["graduation"][data["graduation"]["Demographic"] == "Total Cohort"]


# # Combining the Data Sets

# In[34]:


#Left merge with DBN as the key value
combined = data["sat_results"]
combined = combined.merge(data["ap_2010"], on="DBN", how="left")
combined = combined.merge(data["graduation"], on="DBN", how="left")

#Inner Merge with DBN as the key value and filling Nan values with the mean
to_merge = ["class_size", "demographics", "survey", "hs_directory"]

for m in to_merge:
    combined = combined.merge(data[m], on="DBN", how="inner")

combined = combined.fillna(combined.mean())
combined = combined.fillna(0)

pd.set_option('max_seq_items',300)
combined.columns


# In[17]:


combined.shape


# **The resulting data set has 165 columns in total. As I mentioned earlier, my objective is to determine the relationship between these variables and the SAT score. I  will calculte the correlation coefficient of each of these variables  and analyze in greater detail the most relevant ones.**

# # Data Analysis: Finding Correlations

# In[18]:


# Calculating the correlation between the SAT score and all the other variables

correlations = combined.corr()
sat_correlations = correlations["sat_score"]
correlations_df = pd.DataFrame(sat_correlations).reset_index()
correlations_df.rename(columns={'index':'variable','sat_score':'sat_score correlation'}, inplace=True)
pd.set_option('display.max_rows',None)
correlations_df = correlations_df.sort_values(by='sat_score correlation',ascending = False)
print(pd.DataFrame(correlations_df[correlations_df['sat_score correlation']>0.25]))
print('/n')
print(correlations_df[correlations_df['sat_score correlation']<-0.25])


# # Observations:
# - Some variables of the survey show a significant correlation, of which I can highlight the academic expectations and how safe the schools are perceived to be.
# 
# - The percentage of people who took the Regents and AP exams, and how well the perfomed on it, shows a high correlation with SAT scores.
# 
# - Race shows significant correlations, both positive and negative, depending  which race is taken into account.
# 
# - Regarding which sex predominates in the composition of the classrooms, that is, if there are more women or men, it does not seem to affect the SAT score very significantly.

# # Survey and SAT Score

# In[19]:


# Remove DBN since it's a unique identifier, not a useful numerical value for correlation.
survey_fields.remove("DBN")
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# * rr  = response rate 
# * N = Number of  respondents
# * nr = number of eligible 
# * sf = Safety and Respect
# * com = Communication score based 
# * eng = Engagement score based 
# * aca = Academic expectations 

# In[35]:


#Graphing the Correlations between the survey variables and the SAT scores.
sat_surveyFields_corr = sat_correlations[survey_fields].sort_values(ascending = False)
corr_plot = sat_surveyFields_corr.plot.bar(title="Survey Fields and SAT Scores Correlations",y="C. Coefficient")
plt.show()


# The factors that have a positive correlation above 25 are:
# * Number of parents, students and teacher respondents
# * Academic Expectations based on students response 
# * Safety and respect for teacher and students

# In[21]:


warnings.filterwarnings('ignore')


# ## Safety and Respect for Students

# In[39]:


# Graphing the relationship between Safety and Respect and SAT scores
saf_s_11 = combined[['saf_s_11','sat_score']].astype('int')
print(combined.plot.scatter(x="saf_s_11",y="sat_score",title='Safety and Respect score based on students responses and SAT score'))
plt.show()
print(sns.boxplot(saf_s_11['saf_s_11'],saf_s_11['sat_score'],showmeans=True))
plt.show()


# SAT scores and how safe and respectful are schools according to their students, have a positive correlation of 0.34. When looked at closely, the majority of schools have a saf score between 6 and 7 and an average SAT score around 1200.**However, it should be noted that schools with a saf of 8, which is a minority, registered an average score of 1500 points, a significant difference from lower scoring highschools**

# In[23]:


boro = combined[['borough','saf_s_11','sat_score']]
saf_boro = boro.groupby("borough").agg(numpy.mean).sort_values('saf_s_11',ascending=False)
saf_boro = pd.DataFrame(saf_boro)
saf_boro = saf_boro.reset_index()
saf_boro


# Manhattan and Queens are the safest, bronx and state island in the middle and brooklyn at the bottom.

# ## Academic Expectations based on students response 

# In[38]:


# Graphing the relationship between Students Academic Expectations and SAT scores
aca_s_11 = combined[['aca_s_11','sat_score']].astype('int')
print(combined.plot.scatter(x="aca_s_11",y="sat_score",title='Academic Expectations based on students response and SAT score'))
plt.show()
print(sns.boxplot(aca_s_11['aca_s_11'],saf_s_11['sat_score'],showmeans=True))
plt.show()


# SAT scores and the students’ academic expectations have a positive correlation of 0.34. Most students gave their schools a 7 in terms academic expectations . This group of schools registered an average SAT score of 1200. On the other hand, the same group there shows a lot of outliers, with scores as high as 2000+ mark. Additionally, **schools with an 8 registered an average score around 1400 , the highest one,** even above schools with a 9 in academic expectations, which registered an average SAT close to 1300.

# # Race and SAT score

# In[25]:


# Determining the relationship between race and SAT Score
race_columns = ['white_per','asian_per','black_per','hispanic_per']
print('Race and SAT Score Correlations')
print(correlations['sat_score'][race_columns])
print('\n')
fig = plt.figure(figsize=(15,10))

for sp,race in zip(range(0,4,1),race_columns):
    ax = fig.add_subplot(2,2,sp+1)
    ax.scatter(combined[race],combined['sat_score'])
    ax.set_title('Sat_score and '+str(race)+' Relationship')


# With a correlation of 0.62, the first graph shows how a higher proportion of white students translates into a higher score. A very similar behavior can be seen with asians. On the other hand, quite the opposite happens with blacks and in a greater proportion with hispanics.

# In[26]:


#Creating a Table with schools where more than 95% of their students are Hispanic and their SAT scores 
school_names = combined[['SCHOOL NAME','hispanic_per','sat_score']]
school_names[combined['hispanic_per']>95]


# The schools listed above appear to primarily be geared towards recent immigrants to the US. These schools have a lot of students who are learning English, which could explain the lower SAT scores.

# In[27]:


#Creating a Table with schools where less than 95% of their students are Hispanic and their SAT scores 
schools_less10_hispanic = school_names[combined['hispanic_per']<10]
schools_less10_hispanic[combined['sat_score']>1800]


# Many of the schools above appear to be specialized in science and technology . Aditionally, in order to be addmited an entrance exam is needed,so their  students  already have some experience with standardized tests. This might translate in higher  scores on the SAT.

# # Gender and SAT Score

# In[28]:


# Graphing the relationship between Gender and SAT scores
gender_columns = ['male_per','female_per']
gender_correlations = correlations['sat_score'][gender_columns]
print('Gender and SAT Score Correlations')
print(gender_correlations)
print('\n')

combined.plot.scatter(x='female_per',y='sat_score',title='Female Students % and SAT Scores')
plt.show()

combined.plot.scatter(x='male_per',y='sat_score',title='Male Students % and SAT Scores')
plt.show()


# The majority of schools have an even distribution of male and female students, if one sex  predominates, the difference is around 10%.  These schools registered SAT scores between 1000 and 1400, but some of them registered SAT score outside this range, being 2100  the highest and 900 the lowest.
# Schools where 60% or more of their students are male , registered scores around 1000 and 1900 ; while schools where  60% or more of their students are female, registed SAT scores around 1100 and 1900. Schools where more than 90% of their students were female didn't register a high SAT scores.

# In[29]:


#Research any schools with a female_per greater than 60% and an average SAT score greater than 1700.
names = combined[['SCHOOL NAME','female_per','sat_score']]
names[names['female_per']>60][names['sat_score']>1700]


# These schools appears to be very selective liberal arts schools that have high academic standards.

# # AP Exam Scores vs SAT Scores

# In[30]:


combined["ap_per"] = combined["AP Test Takers "] / combined["total_enrollment"]
test_columns = ['ap_per','Advanced Regents - % of cohort']
combined.plot.scatter(x='ap_per', y='sat_score')
combined.plot.scatter(x='Advanced Regents - % of cohort', y='sat_score')
SAT_AP = combined[['ap_per','Advanced Regents - % of cohort','sat_score']]
SAT_AP_corr = SAT_AP.corr()

SAT_AP_corr = SAT_AP_corr['sat_score'][test_columns]
SAT_AP_corr
print('Correlations of Percentage of AP test takers and Advance Regents with SAT score')
print(SAT_AP_corr)
print('\n')


# The percentage of students who took advanced placement tests and the SAT have a very weak correlation . However, there is a strong correlation between the students who performed well on the AP test and the SAT score.

# # Ranking schools based on their SAT score

# *As a reminder:*
# - More than 1400+ is an excellent score ,
# - Between 1400 and 1300 a very good score,
# - Between 1300 and 1200 a good score,
# - Between 1200 and 1000 enough ,
# - Less than 1000 is considered a bad score .

# In[31]:


# creating a function categorize schools according to their sat score:

def SAT_categorizer(score):
    if score >= 1400:
        return 'Excellent'
    elif score < 1400 and score >= 1300:
        return 'Very Good'
    elif score < 1300 and score >= 1200:
        return 'Good'
    elif score < 1200 and score >= 1000:
        return 'Enough'
    else:
        return 'Bad'

combined['S_Clasification'] = combined['sat_score'].apply(SAT_categorizer)
print(combined['S_Clasification'].value_counts())
combined['S_Clasification'].value_counts().plot.pie()


# In[32]:


survey_columns = ['saf_s_11','aca_s_11']
exam_columns = ['ap_per','Advanced Regents - % of cohort']
columns_of_interest = gender_columns + survey_columns + race_columns + exam_columns + ['sat_score']
print(combined['sat_score'].plot.hist())
combined.groupby('S_Clasification').agg(numpy.mean)[columns_of_interest].sort_values('sat_score',ascending= False)


# Regarding the analysis of variables of interest for the classifications of highschools according to their SAT score:
# 
# - highschools have an equal number of students according to their sex;
# - the average score for the perception of safety and respect according to the students is around 7 points;
# - academic expectations for all high schools is 7;
# - high schools with excellent scores do have predominantly white and asian students;
# - high scoring highschools have mostly black and Hispanic students;
# - on average 70% of the students of highschools that perfomed badly are hispanic;
# - the SAT score data is skewed to the right

# # Conclusion

# Seeking to answer the question of whether the SAT is a discriminatory test, I  just carried out an analysis of  the relationship between different variables and  the SAT score. Variables that showed a significant correlation were the perception of how safe and  respectful the high school is, students academic expectations, race, gender, and the AP examn. I used data from New York City high schools because of its demographic diversity.
# 
# The differences in outcome for the sexes is minimum and high schools were evenly distributed. On the other hand, this is not the case for races, Asians and White seem to perform a lot better than Blacks and Hispanics, but when taking a closer look to the data, I noticed the data is skewed to the right because a lot of high schools with a higher percentage of Asians or white students had an excellent score. Additionally,is important to highlight these high schools have more rigorous acceptance processes. Nevertheless, is also worth noticing that high schools that performed very good, 70% of their students are black or Hispanic. In my opinion, there is not a causal relationship between race and SAT score, the differences in SAT scores between different races is not due to the race, but rather because of cultural differences and barriers such as learning a new language. 
# 
# Additionally, how safe and respectful is a high school environment seem to have a positive impact on sat scores, but there are diminishing returns, schools should only be safe “enough.” When it comes to academic expectations the highest scoring group also have the highest SAT score.On the other hand, variables that initially seem to be important, such as the number of AP exam taken, showed no significant correlation when presented in relative terms with respect to the total number of students, while schools with higher percentage of students that registered high score on the AP exam also performed well on the SAT.
# 
# Author: Hector R. Santos Marte
