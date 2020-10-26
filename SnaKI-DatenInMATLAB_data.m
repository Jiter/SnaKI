%Starte das Skript mit allen Logfiles im selben Ordner


clear

pre_name = "log-20201021-222421_";

files = dir('*.txt');
names = {files.name};
namestrings = string(names);


generation_numbers = numel(namestrings);
generations = (0:1:(generation_numbers -1)).';

name_files = (pre_name + (0:1:(generation_numbers -1)) + ".txt").';
ziel = [];
fields_per_line = 11;  %for example
fmt = repmat('%s',1,fields_per_line);
    
for n = 1 : generation_numbers 

    fid = fopen(name_files(n), 'rt');
    filebycolumn = textscan(fid, fmt, 'Delimiter', ',');
    fclose(fid);
    
    numbers = filebycolumn{:};
    [a b] = size(numbers);
    
    Generation = (((1:1:a)./(1:1:a)).')*n;
   
    fieldarray = horzcat(num2cell(Generation));
    
    
    fieldarray = horzcat(fieldarray, filebycolumn{:});
    
    fieldarray(1,:) = [];
    
    ziel = [ziel; fieldarray];
    

end
