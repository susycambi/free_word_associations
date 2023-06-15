setwd("/Users/susannecambi/Documents/neuroscience_master/Noce_internship/dev/FWA")
data <- read.csv("pivoted_results.csv")
str(data)

# only keep the rows (cue words) for which there are less than 6 zero values (do 6 out of 12 subjects have the file)
# only remove the "flat" cues
data <- data[rowSums(data == 0) < 12, ]


data[data == 0] <- NA
data$mean_count <- rowMeans(data[ , 14:25], na.rm = TRUE)

# mean count by subject
# number of 0 / Na by subject


mean_n_associations <- colMeans(data[ , 14:25], na.rm = T)
n_missing <- colSums(is.na(data[ , 14:25]))
percent_missing <- (colSums(is.na(data[ , 14:25]))/97)*100
subject_stats <- data.frame(n_missing, mean_n_associations, percent_missing)

write.csv(subject_stats, file = "subject_stats.csv")
