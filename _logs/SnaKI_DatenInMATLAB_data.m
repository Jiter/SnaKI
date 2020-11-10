

filePattern = fullfile('./', '*.txt');
files = dir(filePattern);

names= table({files.name}.', 'VariableNames', {'name'});

for k = 1 : numel(names) 

     
    if strfind(files(k).name, "log") 
       name = files(k).name
    end

end



fid = fopen(name);
txt = textscan(fid,'%s','delimiter','\n');
Ziel = [];


for i = 1 : length(txt{1,1})
    
    if strfind(txt{1,1}{i, 1}, "Key:") > 0
        Ziel = [Ziel; convertCharsToStrings(txt{1,1}{i, 1})];
    end
end


Ziel = strrep(Ziel," Key: ", " " )


Ziel_neu = [];
for y = 1: length(Ziel)
    ans = strsplit(Ziel(y), ",");
    Ziel_neu = [Ziel_neu; ans];
end

Ziel_neu = str2double(Ziel_neu)