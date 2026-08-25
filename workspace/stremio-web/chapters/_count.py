import re,sys
t=open(sys.argv[1],encoding="utf-8").read()
cjk=len(re.findall(r"[一-龥]",t))
punc=len(re.findall(r"[，。：；、！？（）【】“”‘’·—…]",t))
print("cjk",cjk,"punc",punc,"total_han+punc",cjk+punc)
