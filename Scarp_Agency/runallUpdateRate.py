from subprocess import call
#files = ['D:\project file\Code project\_1extractSRO.py', 'D:\project file\Code project\_1InsertSRO.py',
#         'D:\project file\Code project\_2extractXNE.py', 'D:\project file\Code project\_2InsertXNE.py',
#         'D:\project file\Code project\_3extractSRG.py', 'D:\project file\Code project\_3InsertSRG.py',
#         'D:\project file\Code project\_4extractTWV.py', 'D:\project file\Code project\_4InsertTWV.py',
#         'D:\project file\Code project\_5extractSME.py', 'D:\project file\Code project\_5InsertSME.py',
#         'D:\project file\Code project\_6extractVSU.py', 'D:\project file\Code project\_6InsertVSU.py',
#         'D:\project file\Code project\_7extractVPC.py', 'D:\project file\Code project\_7InsertVPC.py',
#         'D:\project file\Code project\_8extractK79.py', 'D:\project file\Code project\_8InsertK79.py']

#files = ['D:\project file\Code project\_1InsertSRO.py',
#         'D:\project file\Code project\_2InsertXNE.py',
#         'D:\project file\Code project\_3InsertSRG.py',
#         'D:\project file\Code project\_4InsertTWV.py',
#         'D:\project file\Code project\_5InsertSME.py',
#         'D:\project file\Code project\_6InsertVSU.py',
#         'D:\project file\Code project\_7InsertVPC.py',
#         'D:\project file\Code project\_8InsertK79.py']

files = ['D:\project file\Code project\_1extractSRO.py',
         'D:\project file\Code project\_2extractXNE.py',
         'D:\project file\Code project\_3extractSRG.py',
         'D:\project file\Code project\_4extractTWV.py',
         'D:\project file\Code project\_5extractSME.py',
         'D:\project file\Code project\_6extractVSU.py',
         'D:\project file\Code project\_7extractVPC.py',
         'D:\project file\Code project\_8extractK79.py',]


for f in files:
    call(["python", f])
    print(f + "  =====================================")

